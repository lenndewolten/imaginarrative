using 'story-teller.bicep'

param containerAppEnvName = 'harmony-env'
param containerAppEnvRG = 'Harmony'

param acrName = 'lenndewoltenharmony'
param acrRG = 'Harmony'

param storageAccountName = 'storytellerstrg'

param containerAppName = 'story-teller'

param image = {
  repository: 'story-teller'
  tag: 'v1'
}
