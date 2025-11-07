from __future__ import annotations

from pydantic import BaseModel, Field, ValidationError
import re


PII_EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
PII_PHONE = re.compile(r"\+?\d[\d\-\s]{7,}\d")


def scrub_pii(text: str) -> str:
    text = PII_EMAIL.sub("[REDACTED_EMAIL]", text)
    text = PII_PHONE.sub("[REDACTED_PHONE]", text)
    return text


class AssessmentGuard(BaseModel):
    score: float = Field(ge=0, le=100)
    skill_matching_score: float = Field(ge=0, le=100)
    total_experience_matching_score: float = Field(ge=0, le=100)
    relevant_experience_matching_score: float = Field(ge=0, le=100)
    educational_matching_score: float = Field(ge=0, le=100)
    rationale: str
    strengths: list[str]
    gaps: list[str]
    recommendations: list[str]
    objectivity_evidence: list[str]


def enforce_assessment_guard(payload: dict) -> dict:
    try:
        payload["rationale"] = scrub_pii(payload.get("rationale", ""))
        payload["strengths"] = [scrub_pii(s) for s in payload.get("strengths", [])]
        payload["gaps"] = [scrub_pii(s) for s in payload.get("gaps", [])]
        payload["recommendations"] = [scrub_pii(s) for s in payload.get("recommendations", [])]
        payload["objectivity_evidence"] = [scrub_pii(s) for s in payload.get("objectivity_evidence", [])]
        return AssessmentGuard(**payload).model_dump()
    except ValidationError as e:
        raise ValueError(f"Assessment failed guard validation: {e}")


