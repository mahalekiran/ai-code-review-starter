# Deploy to AWS App Runner

AWS App Runner is a simple option for deploying containerized web APIs without managing servers.

## Prerequisites
- AWS CLI
- Docker Desktop
- ECR repositories for both services

## Basic deployment path

1. Build Docker images for both services.
2. Push images to Amazon ECR.
3. Create two App Runner services:
   - Python AI service
   - .NET API service
4. Set environment variables:
   - Python service: `OPENAI_API_KEY`, `OPENAI_MODEL`
   - .NET service: `AI_SERVICE_URL=https://<python-service-url>`

Official reference: https://docs.aws.amazon.com/apprunner/latest/dg/service-source-image.html
