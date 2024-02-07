$rg = "Image-Captioning"
$location = "eastus"
$acrName = "lenndewoltenharmony"

$imageName = "image-captioning"
$imageTag = "v1"
az account set --name 7ba9e6b6-7591-4828-aaa5-c4656cb871c3

docker build -t "$($imageName):$($imageTag)" ../
docker tag "$($imageName):$($imageTag)"   "$($acrName).azurecr.io/$($imageName):$($imageTag)"

az acr login -n $acrName
docker push "$($acrName).azurecr.io/$($imageName):$($imageTag)"

az group create -n $rg --location $location = "eastus"
az deployment group create --resource-group $rg --template-file .\image-captation.bicep  --parameters .\image-captation.bicepparam


az account set --name e84d14c9-e150-4500-93b2-5aa2829e295d