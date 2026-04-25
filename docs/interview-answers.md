# Interview Answers for AI-Powered Secure Code Review Assistant

## 1. Tell me about your AI project.
I built an AI-powered secure code review assistant to review C#/.NET code for security, performance, reliability, and maintainability issues. The solution uses a .NET Web API as the main application layer and a Python FastAPI service as the AI layer. The .NET API accepts code input and calls the Python AI service, which sends a structured prompt to an LLM and returns findings in JSON format.

## 2. Why did you choose this project?
My background is in .NET, DevOps, secure development, SonarQube, and code quality. This project connects my existing strengths with GenAI. Instead of building a generic chatbot, I built something relevant to real engineering teams: AI-assisted code review.

## 3. How do you validate AI output?
I do not treat AI output as automatically correct. I validate it using human code review, rule-based checks for common issues such as SQL injection, and structured JSON output. In a production version, I would add automated tests, SonarQube comparison, severity thresholds, and feedback loops.

## 4. What are the risks?
The main risks are hallucinated findings, missed vulnerabilities, exposure of sensitive source code, and inconsistent output. To reduce these risks, I would use prompt constraints, JSON schema validation, source-code masking, private model deployment, and mandatory human approval before applying fixes.

## 5. How is this different from SonarQube?
SonarQube is strong for deterministic static rules. The AI layer adds reasoning and contextual explanation. The best approach is not to replace SonarQube but to combine both: rules for consistency and AI for explanation, remediation guidance, and edge-case review.

## 6. How would you productionize it?
I would add authentication, role-based access, audit logging, secret scanning, source-code redaction, queue-based processing, persistent storage for review results, observability dashboards, CI/CD integration, and deployment to Azure Container Apps or AWS App Runner.

## 7. How does this show AI-first engineering?
The project demonstrates AI-assisted engineering by using an LLM as part of the software delivery workflow. It also shows how to design guardrails around AI output through structured prompts, schema validation, fallback checks, and human review.
