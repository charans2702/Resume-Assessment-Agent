from __future__ import annotations

from typing import Dict, Any
from app.utils.config import settings
from app.utils.gemini import generate_json
from app.utils.agno import build_gemini_agent
from datetime import datetime, timezone

ASSESS_SYSTEM = (
    "Role: Objective resume assessor.\n"
    "Task: Compare parsed resume and raw text against the Job Description.\n"
    f"Use this Current Date: {datetime.now(timezone.utc).isoformat()}\n for calculating experience durations.\n"
    "Output JSON with fields (numbers 0-100):\n"
    "- score: overall fit.\n"
    "- skill_matching_score: match of required vs present skills.\n"
    "- total_experience_matching_score: total years vs JD requirement.\n"
    "- relevant_experience_matching_score: years in relevant roles/tech.\n"
    "- educational_matching_score: degree/cert alignment.\n"
    "- rationale: concise explanation with evidence.\n"
    "- strengths[]: bullet points grounded in resume.\n"
    "- gaps[]: bullet points of missing/weak areas.\n"
    "- recommendations[]: concrete ways to improve the resume for this JD.\n"
    "- objectivity_evidence[]: short quotes/facts from resume/JD supporting scores.\n"
    "Rules: Be deterministic and grounded; no speculation; output ONLY JSON."
)


def assess_resume(parsed: Dict[str, Any], resume_text: str, job_description: str, retrieved_context: list[str]) -> Dict[str, Any]:
    if not settings.gemini_api_key:
        # Basic heuristic fallback without LLM
        skills = parsed.get("skills", [])
        hit = sum(1 for s in skills if s and s.lower() in job_description.lower())
        score = min(100.0, float(hit * 10))
        return {
            "score": score,
            "skill_matching_score": min(100.0, float(hit * 10)),
            "total_experience_matching_score": 50.0,
            "relevant_experience_matching_score": 50.0,
            "educational_matching_score": 50.0,
            "rationale": "Heuristic overlap-based estimate.",
            "strengths": skills[:3],
            "gaps": [],
            "recommendations": ["Add measurable impact and align skills to JD keywords."],
            "objectivity_evidence": ["Keyword overlap used."],
        }

    import json
    context = "\n\n".join(retrieved_context[:5])
    user = json.dumps({
        "parsed": parsed,
        "resume_text": resume_text[:4000],
        "job_description": job_description[:4000],
        "retrieved": context[:2000],
    })
    data = None
    agent = build_gemini_agent(ASSESS_SYSTEM)
    if agent is not None:
        try:
            out = agent.run(user)
            text = (out.content or "").strip()
            data = json.loads(text) if text else None
        except Exception:
            data = None
    if not data:
        data = generate_json(ASSESS_SYSTEM, user) or {
        "score": 50.0,
        "skill_matching_score": 50.0,
        "total_experience_matching_score": 50.0,
        "relevant_experience_matching_score": 50.0,
        "educational_matching_score": 50.0,
        "rationale": "Fallback response format.",
        "strengths": [],
        "gaps": [],
        "recommendations": [],
        "objectivity_evidence": [],
    }
    return data


