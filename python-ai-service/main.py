import json
import os
from typing import List, Optional

from fastapi import FastAPI, HTTPException
from openai import OpenAI
from pydantic import BaseModel, Field

app = FastAPI(title="AI Code Review Service", version="1.0.0")


class CodeReviewRequest(BaseModel):
    fileName: str
    language: str = "csharp"
    code: str


class CodeReviewFinding(BaseModel):
    severity: str = Field(description="Critical, Major, Minor, Info")
    category: str = Field(description="Security, Performance, Reliability, Maintainability, Testing")
    description: str
    suggestedFix: str
    lineNumber: Optional[int] = None


class CodeReviewResponse(BaseModel):
    summary: str
    findings: List[CodeReviewFinding]


SYSTEM_PROMPT = """
You are a senior .NET principal engineer and secure code reviewer.
Review C#/.NET code for security, performance, reliability, maintainability, and testing gaps.
Return only valid JSON. Do not include markdown.
Schema:
{
  "summary": "short overall summary",
  "findings": [
    {
      "severity": "Critical|Major|Minor|Info",
      "category": "Security|Performance|Reliability|Maintainability|Testing",
      "description": "clear issue description",
      "suggestedFix": "specific fix recommendation",
      "lineNumber": 1
    }
  ]
}
Rules:
- Be practical and specific.
- Do not invent line numbers if unsure; use null.
- Prefer secure-by-default .NET recommendations.
- Flag SQL injection, hardcoded secrets, weak exception handling, missing async usage, missing cancellation tokens, and inefficient queries when applicable.
"""


def fallback_review(request: CodeReviewRequest) -> CodeReviewResponse:
    findings: List[CodeReviewFinding] = []
    code_lower = request.code.lower()

    if "select" in code_lower and "+" in request.code:
        findings.append(CodeReviewFinding(
            severity="Critical",
            category="Security",
            description="Possible SQL injection risk because SQL appears to be built using string concatenation.",
            suggestedFix="Use parameterized queries, stored procedures with parameters, or an ORM query API such as EF Core LINQ.",
            lineNumber=None,
        ))

    if "catch" in code_lower and "throw;" not in code_lower:
        findings.append(CodeReviewFinding(
            severity="Minor",
            category="Reliability",
            description="Exception handling may hide original exception details.",
            suggestedFix="Log the exception with context and rethrow using 'throw;' where appropriate.",
            lineNumber=None,
        ))

    if not findings:
        findings.append(CodeReviewFinding(
            severity="Info",
            category="Maintainability",
            description="No obvious high-risk issue detected by fallback rule-based review.",
            suggestedFix="Run AI review with OPENAI_API_KEY configured for deeper analysis.",
            lineNumber=None,
        ))

    return CodeReviewResponse(summary="Fallback rule-based review completed.", findings=findings)


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/analyze", response_model=CodeReviewResponse)
def analyze(request: CodeReviewRequest):
    if not request.code.strip():
        raise HTTPException(status_code=400, detail="Code is required.")

    api_key = os.getenv("OPENAI_API_KEY")
    model = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")

    if not api_key or api_key == "replace-with-your-key":
        return fallback_review(request)

    client = OpenAI(api_key=api_key)

    user_prompt = f"""
File: {request.fileName}
Language: {request.language}

Code:
{request.code}
"""

    try:
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.1,
            response_format={"type": "json_object"},
        )

        content = completion.choices[0].message.content or "{}"
        parsed = json.loads(content)
        return CodeReviewResponse(**parsed)
    except Exception as exc:
        # Keep the app demo-friendly; in production, log this with correlation ID.
        return CodeReviewResponse(
            summary=f"AI review failed; fallback review used. Reason: {str(exc)}",
            findings=fallback_review(request).findings,
        )
