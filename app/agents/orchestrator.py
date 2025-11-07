from __future__ import annotations

from sqlalchemy.orm import Session
from typing import Dict, Any
from app.agents.parser_agent import parse_resume_with_llm
from app.agents.assessor_agent import assess_resume
from app.agents.critic_agent import critique_assessment
from app.rag.retriever import retrieve_context
from app.guardrails.validators import enforce_assessment_guard
from app.db import crud
import re



def run_assessment_pipeline(db: Session, job_id: str, resume_id: str, resume_text: str, job_description: str) -> Dict[str, Any]:
    parsed = parse_resume_with_llm(resume_text)
    retrieved = retrieve_context(resume_text, job_description, top_k=5)
    assessment = assess_resume(parsed, resume_text, job_description, retrieved)
    critique = critique_assessment(assessment, resume_text, job_description)
    final = critique.get("corrected", assessment)
    final = enforce_assessment_guard(final)

    # Extract candidate identity and persist
    candidate_name = parsed.get("name") if isinstance(parsed, dict) else None
    # try from parsed or fallback regex
    candidate_email = None
    if isinstance(parsed, dict):
        candidate_email = parsed.get("email") or None
    if not candidate_email:
        m = re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", resume_text)
        candidate_email = m.group(0) if m else None
    try:
        crud.upsert_resume_identity(db, resume_id=resume_id, job_id=job_id, candidate_name=candidate_name, candidate_email=candidate_email)
    except Exception:
        pass

    created = crud.create_assessment(
        db,
        resume_id=resume_id,
        score=float(final["score"]),
        skill_matching_score=float(final.get("skill_matching_score", 0.0)),
        total_experience_matching_score=float(final.get("total_experience_matching_score", 0.0)),
        relevant_experience_matching_score=float(final.get("relevant_experience_matching_score", 0.0)),
        educational_matching_score=float(final.get("educational_matching_score", 0.0)),
        rationale=final["rationale"],
        strengths=final.get("strengths", []),
        gaps=final.get("gaps", []),
        recommendations=final.get("recommendations", []),
        objectivity_evidence=final.get("objectivity_evidence", []),
    )
    return {
        "assessment_id": created.id,
        "candidate_name": candidate_name,
        "candidate_email": candidate_email,
        "score": created.score,
        "skill_matching_score": created.skill_matching_score,
        "total_experience_matching_score": created.total_experience_matching_score,
        "relevant_experience_matching_score": created.relevant_experience_matching_score,
        "educational_matching_score": created.educational_matching_score,
        "rationale": created.rationale,
        "strengths": final.get("strengths", []),
        "gaps": final.get("gaps", []),
        "recommendations": final.get("recommendations", []),
        "objectivity_evidence": final.get("objectivity_evidence", []),
    }


