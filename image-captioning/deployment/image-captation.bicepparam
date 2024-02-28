using 'image-captation.bicep'

param containerAppEnvName = 'harmony-env'
param containerAppEnvRG = 'Harmony'

param acrName = 'lenndewoltenharmony'
param acrRG = 'Harmony'

param storageAccountName = 'imagecaptioningstrg'

param containerAppName = 'image-captioning'

param image = {
  repository: 'image-captioning'
  tag: 'v1'
}
