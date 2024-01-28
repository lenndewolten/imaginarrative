az account set --name 7ba9e6b6-7591-4828-aaa5-c4656cb871c3

az group create -n Harmony --location eastus
az deployment group create --resource-group Harmony --template-file .\container-app-environment.bicep  --parameters .\container-app-environment.bicepparam

az group create -n Image-Captioning --location eastus
az deployment group create --resource-group Image-Captioning --template-file .\image-captation.bicep  --parameters .\image-captation.bicepparam

az acr import `
    --name lenndewoltentestacr `
    --source mcr.microsoft.com/azuredocs/containerapps-helloworld:latest `
    --image containerapps-helloworld:latest

az acr import `
    --name lenndewoltentestacr `
    --source docker.io/lenndewolten/azure-tests:storageaccounttest `
    --image containerapps-storageaccount:v2

az acr repository list --name lenndewoltentestacr 

az account set --name e84d14c9-e150-4500-93b2-5aa2829e295d