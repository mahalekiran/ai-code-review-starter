# Deploy to Azure Container Apps

Azure Container Apps is a good fit because this project is containerized and does not require managing Kubernetes.

## Prerequisites
- Azure CLI
- Docker Desktop
- Azure subscription

## Basic deployment path

```bash
az login
az group create --name rg-ai-code-review --location eastus
az acr create --resource-group rg-ai-code-review --name <uniqueacrname> --sku Basic
az acr login --name <uniqueacrname>

docker build -t <uniqueacrname>.azurecr.io/ai-python-service:1.0 ./python-ai-service
docker push <uniqueacrname>.azurecr.io/ai-python-service:1.0

docker build -t <uniqueacrname>.azurecr.io/ai-dotnet-api:1.0 ./dotnet-api
docker push <uniqueacrname>.azurecr.io/ai-dotnet-api:1.0
```

Create Container Apps environment and deploy Python service first, then .NET API with `AI_SERVICE_URL` pointing to the Python service URL.

For demo simplicity, you can also use `az containerapp up` from each service folder.

Official reference: https://learn.microsoft.com/azure/container-apps/containerapp-up
