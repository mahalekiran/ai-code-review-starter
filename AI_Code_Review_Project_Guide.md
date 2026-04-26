# AI-Powered Secure Code Review Assistant - Project Guide

## 1. Project Overview

The **AI-Powered Secure Code Review Assistant** is a practical developer productivity and DevSecOps project built using **.NET 8 Web API**, **Python FastAPI**, **Docker**, and an optional **OpenAI-compatible LLM API**.

The project analyzes C#/.NET source code and returns structured feedback such as:

- Security issues
- Code quality issues
- Performance concerns
- Suggested fixes
- Severity/category-based review comments

This project is designed to complement existing tools such as **SonarQube**, not replace them. SonarQube is strong for static rule-based checks, while this AI assistant can explain issues, suggest remediation, and identify review points that need human judgment.

---

## 2. Business Value

### 2.1 Improves Code Review Efficiency

Manual code reviews take time, especially when senior developers are overloaded. This tool provides an initial AI-assisted review so developers can fix common issues before human review.

**Business benefit:** Faster pull request turnaround and reduced dependency on senior reviewers for basic issues.

---

### 2.2 Enhances Secure Coding Practices

The tool can identify common risky patterns such as:

- SQL injection risk
- Hardcoded secrets
- Missing input validation
- Weak exception handling
- Poor logging practices

**Business benefit:** Helps reduce security defects earlier in the development lifecycle.

---

### 2.3 Supports DevSecOps Shift-Left Approach

The project can be integrated into CI/CD pipelines so code can be reviewed before deployment.

**Business benefit:** Security and quality checks happen earlier, reducing rework during QA/UAT/production.

---

### 2.4 Reduces Production Defects

By catching code smells, insecure code, and maintainability issues early, teams can reduce production incidents.

**Business benefit:** Better quality, fewer defects, and improved system reliability.

---

### 2.5 Helps Teams Adopt AI-Assisted Engineering

This project demonstrates practical usage of AI in the software delivery lifecycle.

**Business benefit:** Shows how AI can be used responsibly for developer productivity, code quality, and engineering governance.

---

## 3. Real-World Usage

This project can be used in multiple ways.

### Option 1: Manual Code Review

A developer copies a C# code block and submits it through Swagger/Postman. The API returns AI-assisted review comments.

Use case:

- Developer wants quick review before committing code
- Lead wants to validate risky logic quickly
- Junior developer wants explanation and suggestions

---

### Option 2: CI/CD Pipeline Integration

The project can be called from Azure DevOps, Jenkins, GitHub Actions, or GitLab CI.

Use case:

- During build pipeline, changed files are sent to the AI review API
- If critical/high severity issues are found, the pipeline can fail or warn
- Review results can be attached as build output

---

### Option 3: GitHub Pull Request Review

The tool can be extended to analyze changed files in a pull request and post comments back to GitHub.

Use case:

- Developer raises PR
- GitHub Action calls AI Code Review API
- AI review comments appear on the PR
- Human reviewer validates final decision

---

### Option 4: Internal Engineering Governance

Technical leads can use the system to enforce secure coding and architecture standards.

Use case:

- Validate coding practices
- Identify repeated mistakes
- Improve developer learning
- Support code review checklist automation

---

## 4. High-Level Architecture

```text
Developer / Pipeline / GitHub PR
        |
        v
.NET 8 Web API
        |
        v
Python FastAPI AI Service
        |
        v
OpenAI-compatible LLM API / Rule-based fallback
```

### Components

| Component | Purpose |
|---|---|
| .NET 8 Web API | Main API exposed to users/pipelines |
| Python FastAPI Service | AI processing layer |
| OpenAI API | Optional LLM-based code analysis |
| Docker Compose | Runs both services together locally |
| Swagger | API testing interface |

---

## 5. Folder Structure

```text
ai-code-review-starter
│
├── dotnet-api
│   ├── Controllers
│   ├── Models
│   ├── Services
│   ├── Program.cs
│   └── Dockerfile
│
├── python-ai-service
│   ├── main.py
│   ├── requirements.txt
│   └── Dockerfile
│
├── docker-compose.yml
├── README.md
├── Azure-Deployment.md
├── AWS-Deployment.md
├── Interview-Answers.md
└── Resume-Section.md
```

---

## 6. Prerequisites

Install the following tools:

- .NET 8 SDK
- Python 3.11 or above
- Docker Desktop
- Git
- Visual Studio 2022 or Visual Studio Code
- Azure CLI, if deploying to Azure
- AWS CLI, if deploying to AWS

Verify installation:

```powershell
dotnet --version
python --version
docker --version
git --version
az --version
aws --version
```

---

## 7. How to Run Without Docker

Use this option when you want to debug services separately.

### 7.1 Run Python AI Service

Open PowerShell:

```powershell
cd "E:\Projects\AI project\ai-code-review-starter\python-ai-service"
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

Open in browser:

```text
http://localhost:8000/docs
```

This should open FastAPI documentation.

---

### 7.2 Run .NET API

Open another PowerShell window:

```powershell
cd "E:\Projects\AI project\ai-code-review-starter\dotnet-api"
dotnet restore
dotnet build
$env:ASPNETCORE_ENVIRONMENT="Development"
dotnet run
```

Open in browser:

```text
http://localhost:5000/swagger
```

Important:

- Keep the terminal running.
- Do not close the terminal while testing.
- If Swagger does not open, confirm the port shown in the console.

---

## 8. How to Run With Docker Compose

Use this option to run the full project as containers.

From project root:

```powershell
cd "E:\Projects\AI project\ai-code-review-starter"
docker compose down
docker compose up --build
```

Based on your current `docker-compose.yml`:

```yaml
services:
  dotnet-api:
    build: ./dotnet-api
    ports:
      - "5000:8080"
    environment:
      - AI_SERVICE_URL=http://python-ai-service:8000
    depends_on:
      - python-ai-service

  python-ai-service:
    build: ./python-ai-service
    ports:
      - "8000:8000"
```

Open:

```text
.NET API Swagger: http://localhost:5000/swagger
Python FastAPI Docs: http://localhost:8000/docs
```

Do **not** use `http://localhost:8080/swagger` because port 8080 may already be used by Jenkins on your machine.

---

## 9. How to Test the Project

Open Swagger:

```text
http://localhost:5000/swagger
```

Find the API endpoint similar to:

```http
POST /api/code-review/analyze
```

Use this sample request:

```json
{
  "fileName": "UserRepository.cs",
  "language": "csharp",
  "code": "public void GetUser(string id) { var query = \"SELECT * FROM Users WHERE Id = '\" + id + \"'\"; }"
}
```

Expected response should include review issues such as:

```json
{
  "issues": [
    {
      "severity": "High",
      "category": "Security",
      "description": "Possible SQL injection risk due to dynamic SQL string concatenation.",
      "recommendation": "Use parameterized queries or stored procedures."
    }
  ]
}
```

---

## 10. How to Use With an Existing .NET Project

### 10.1 Manual Usage

Copy any class/method from your existing .NET project and send it to the API using Swagger or Postman.

Example:

```json
{
  "fileName": "PaymentService.cs",
  "language": "csharp",
  "code": "paste your C# code here"
}
```

Review the output and fix issues manually.

---

### 10.2 Use in Development Workflow

Recommended developer workflow:

```text
Write code
   ↓
Run unit tests
   ↓
Send important/risky code to AI Code Review API
   ↓
Fix suggested issues
   ↓
Raise PR
   ↓
Human review + SonarQube review
```

---

### 10.3 Use in CI/CD Pipeline

You can call the API from a pipeline script.

Example concept:

```powershell
$code = Get-Content "src/MyProject/Services/UserService.cs" -Raw

$body = @{
    fileName = "UserService.cs"
    language = "csharp"
    code = $code
} | ConvertTo-Json

Invoke-RestMethod `
    -Uri "http://localhost:5000/api/code-review/analyze" `
    -Method Post `
    -Body $body `
    -ContentType "application/json"
```

Later, this can be extended to:

- Scan only changed files
- Fail build for high severity issues
- Publish report as pipeline artifact
- Comment on pull request

---

## 11. Debugging Guide

### 11.1 Debug .NET API

In Visual Studio:

1. Open the `.csproj` file from `dotnet-api`.
2. Set `ASPNETCORE_ENVIRONMENT=Development`.
3. Put breakpoint in controller/service.
4. Press F5.
5. Call API from Swagger.

If you get file lock error:

```text
Could not copy apphost.exe...
The file is locked by AiCodeReview.Api
```

Fix:

```powershell
taskkill /PID <PID> /F
```

Or close any terminal where `dotnet run` is already running.

---

### 11.2 Debug Python Service

Run:

```powershell
cd "E:\Projects\AI project\ai-code-review-starter\python-ai-service"
.venv\Scripts\activate
uvicorn main:app --reload --port 8000
```

Open:

```text
http://localhost:8000/docs
```

Add breakpoints in VS Code or add temporary `print()` statements.

---

### 11.3 Common Port Issues

| URL | Expected Application |
|---|---|
| http://localhost:5000/swagger | .NET API |
| http://localhost:8000/docs | Python FastAPI Service |
| http://localhost:8080 | Jenkins on your machine |

If Jenkins opens on port 8080, that is expected because Jenkins is already running on that port.

---

## 12. OpenAI API Key Configuration

The project can run with fallback logic, but for real LLM review, set the API key.

Temporary PowerShell setting:

```powershell
$env:OPENAI_API_KEY="your_api_key_here"
```

Permanent Windows setting:

```powershell
setx OPENAI_API_KEY "your_api_key_here"
```

After using `setx`, close and reopen PowerShell.

For Docker:

```powershell
$env:OPENAI_API_KEY="your_api_key_here"
docker compose up --build
```

Do not commit real API keys to GitHub.

---

## 13. GitHub Check-in Steps

### 13.1 Add `.gitignore`

Create `.gitignore` in project root:

```gitignore
.vs/
bin/
obj/
*.user
*.suo
.env
.venv/
__pycache__/
```

---

### 13.2 Initialize and Commit

```powershell
cd "E:\Projects\AI project\ai-code-review-starter"
git init
git add .
git commit -m "Initial commit - AI powered code review assistant"
```

---

### 13.3 Push to GitHub

Create an empty GitHub repository, then run:

```powershell
git branch -M main
git remote add origin https://github.com/<your-username>/ai-code-review-assistant.git
git push -u origin main
```

---

## 14. Azure Deployment - High-Level Steps

Recommended Azure service: **Azure Container Apps**.

### Steps

1. Create Azure Resource Group
2. Create Azure Container Registry
3. Build Docker images
4. Push images to ACR
5. Create Container Apps Environment
6. Deploy Python AI service internally
7. Deploy .NET API externally
8. Configure environment variables/secrets

High-level commands:

```powershell
az login
az group create --name rg-ai-code-review --location eastus
az acr create --resource-group rg-ai-code-review --name aicodereviewacr --sku Basic
az acr login --name aicodereviewacr
```

Build and push images:

```powershell
docker build -t aicodereviewacr.azurecr.io/dotnet-api:v1 ./dotnet-api
docker build -t aicodereviewacr.azurecr.io/python-ai-service:v1 ./python-ai-service

docker push aicodereviewacr.azurecr.io/dotnet-api:v1
docker push aicodereviewacr.azurecr.io/python-ai-service:v1
```

Production note:

- Store `OPENAI_API_KEY` as a secret.
- Keep Python service internal if possible.
- Expose only the .NET API publicly.

---

## 15. AWS Deployment - High-Level Steps

Recommended AWS service: **AWS App Runner** or **ECS Fargate**.

### Steps

1. Create ECR repositories
2. Build Docker images
3. Push images to ECR
4. Create App Runner service for .NET API
5. Create App Runner service for Python AI service
6. Configure environment variables
7. Secure API keys using AWS Secrets Manager if moving toward production

High-level commands:

```powershell
aws configure
aws ecr create-repository --repository-name ai-code-review-dotnet-api
aws ecr create-repository --repository-name ai-code-review-python-service
```

Build images:

```powershell
docker build -t ai-code-review-dotnet-api ./dotnet-api
docker build -t ai-code-review-python-service ./python-ai-service
```

Push to ECR after tagging with your AWS account ECR URL.

Production note:

- Do not expose Python service publicly unless required.
- Store API keys securely.
- Enable logs and monitoring.

---

## 16. How to Explain This Project in Interview

### Short Explanation

I built an AI-powered secure code review assistant using .NET 8 and Python FastAPI. The .NET API accepts source code and passes it to a Python AI service, which analyzes the code for security, performance, and quality issues. The result is returned as structured review feedback with severity and recommendations.

---

### Business Explanation

The business value is to reduce manual code review effort, identify security issues earlier, and support DevSecOps shift-left practices. It can be integrated into CI/CD pipelines or PR workflows so developers receive feedback before code reaches QA or production.

---

### Technical Explanation

The project uses a service-based architecture:

- .NET 8 Web API as the main interface
- Python FastAPI as the AI analysis layer
- Docker Compose for local orchestration
- Optional OpenAI-compatible LLM integration
- Rule-based fallback if LLM API key is not configured

---

### Responsible AI Explanation

AI output is treated as an assistant, not as final approval. Human review is still required. The project is designed to complement SonarQube and manual review, not replace them.

---

## 17. Resume Usage After Completing the Project

Use this only after you have run and tested the project successfully.

```text
Built an AI-powered secure code review assistant using .NET 8, Python FastAPI, Docker, and LLM integration to analyze C# code for security, performance, and code quality issues, providing structured recommendations to support DevSecOps shift-left practices.
```

Alternative shorter version:

```text
Developed an AI-assisted code review tool using .NET 8 and Python FastAPI to identify security, performance, and maintainability issues in C# code before pull request review.
```

---

## 18. Future Enhancements

Recommended next improvements:

1. GitHub Pull Request integration
2. Azure DevOps pipeline integration
3. SonarQube result comparison
4. HTML/PDF review report generation
5. Severity-based build failure
6. Authentication for API access
7. SQL Server storage for scan history
8. Dashboard for review metrics
9. Support for multiple languages
10. Prompt versioning and evaluation

---

## 19. Key Takeaway

This project shows practical AI usage in a .NET engineering environment. It demonstrates how a senior .NET/DevOps engineer can adopt AI-first engineering practices while still maintaining secure, controlled, and reviewable software delivery.
