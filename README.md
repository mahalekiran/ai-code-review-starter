# AI-Powered Secure Code Review Assistant

A practical starter project for a .NET + DevSecOps engineer to demonstrate real GenAI/AI-first engineering experience.

## What it does
- Accepts C# code through a .NET Web API
- Sends the code to a Python FastAPI AI service
- Uses an LLM to review code for security, performance, reliability, and maintainability issues
- Returns structured JSON findings
- Includes Docker Compose for local execution

## Architecture

Client/Postman -> .NET 8 Web API -> Python FastAPI AI Service -> OpenAI-compatible LLM API

## Run locally

### Prerequisites
- .NET 8 SDK
- Python 3.11+
- Docker Desktop
- OpenAI API key or Azure OpenAI-compatible endpoint changes

### Option 1: Docker Compose

```bash
cd ai-code-review-starter
copy .env.example .env
# edit .env and set OPENAI_API_KEY

docker compose up --build
```

.NET API: http://localhost:5000/swagger
Python AI Service: http://localhost:8000/docs

### Test request

```bash
curl -X POST http://localhost:5000/api/code-review/analyze \
  -H "Content-Type: application/json" \
  -d @sample-request.json
```

## Resume-safe positioning
This project can be shown as a self-built GenAI engineering project. Do not claim production/client usage unless actually deployed and used in a real environment.
