$rg = "Harmony"
$location = "eastus"

az account set --name 7ba9e6b6-7591-4828-aaa5-c4656cb871c3

az group create -n $rg --location $location
az deployment group create --resource-group $rg --template-file .\container-app-environment.bicep  --parameters .\container-app-environment.bicepparam

az account set --name e84d14c9-e150-4500-93b2-5aa2829e295d