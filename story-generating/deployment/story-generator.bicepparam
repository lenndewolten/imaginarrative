using 'story-generator.bicep'

param containerAppEnvName = 'harmony-env'
param containerAppEnvRG = 'Harmony'

param acrName = 'lenndewoltenharmony'
param acrRG = 'Harmony'

param containerAppName = 'story-generator'

param image = {
  repository: 'story-generator'
  tag: 'v1'
}
