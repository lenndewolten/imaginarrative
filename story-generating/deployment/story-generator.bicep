@description('Provide a location for the container resources.')
param location string = resourceGroup().location

@description('Provide a name for the container environment.')
param containerAppEnvName string
@description('Provide the resource group for the container environment.')
param containerAppEnvRG string

@description('Provide a name of your Azure Container Registry')
param acrName string
@description('Provide the resource group for the container environment.')
param acrRG string

@description('Provide a name for the container app.')
param containerAppName string

@description('Provide a name of the managed identity.')
param identityName string = '${containerAppName}-identity'

@description('Provide the tag of the image used by the app.')
param image Image = {
  repository: 'image-captioning'
  tag: 'latest'
}

param secrets Secret[] = []

var acrPullRole = '7f951dda-4ed3-4680-a7ca-43fe172d538d'

resource identity 'Microsoft.ManagedIdentity/userAssignedIdentities@2023-01-31' = {
  name: identityName
  location: location
}

module containerApp_identity_acrPullRole '../../deployment/modules/role-assignments.bicep' = {
  name: 'container-app-acr-access-${containerAppName}'
  scope: resourceGroup(acrRG)
  params: {
    principalId: identity.properties.principalId
    roleDefinitionId: acrPullRole
  }
}

resource acr 'Microsoft.ContainerRegistry/registries@2023-01-01-preview' existing = {
  name: acrName
  scope: resourceGroup(acrRG)
}

resource containerAppEnv 'Microsoft.App/managedEnvironments@2023-05-01' existing = {
  name: containerAppEnvName
  scope: resourceGroup(containerAppEnvRG)
}

var targetPort = 8000
var env = [for secret in secrets: {
  name: secret.name
  value: secret.value
}]

resource containerApp 'Microsoft.App/containerApps@2023-05-01' = {
  name: containerAppName
  location: location
  identity: {
    type: 'UserAssigned'
    userAssignedIdentities: {
      '${identity.id}': {}
    }
  }
  properties: {
    configuration: {
      ingress: {
        external: true
        targetPort: targetPort
      }
      registries: [
        {
          identity: identity.id
          server: acr.properties.loginServer
        }
      ]
      secrets: secrets
    }
    environmentId: containerAppEnv.id

    template: {
      containers: [
        {
          image: '${acr.properties.loginServer}/${image.repository}:${image.tag}'
          name: containerAppName
          resources: {
            cpu: json('0.25')
            memory: '0.5Gi'
          }
          env: env
          probes: [
            {
              failureThreshold: 10
              httpGet: {
                path: 'ready'
                port: targetPort
                scheme: 'HTTP'
              }
              initialDelaySeconds: 30
              periodSeconds: 30
              timeoutSeconds: 10
              type: 'Readiness'
            }
            {
              httpGet: {
                path: 'live'
                port: targetPort
                scheme: 'HTTP'
              }
              periodSeconds: 60
              timeoutSeconds: 10
              type: 'Liveness'
            }
          ]
        }

      ]
      scale: {
        minReplicas: 0
        maxReplicas: 5
        rules: [
          {
            name: 'http-requests'
            http: {
              metadata: {
                concurrentRequests: '1'
              }
            }
          }
        ]
      }
    }
  }
}

type Image = {
  repository: string
  tag: string
}

type Secret = {
  name: string
  value: string
}
