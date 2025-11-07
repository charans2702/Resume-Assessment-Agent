from __future__ import annotations

from typing import Dict, Any
from app.utils.config import settings
from app.utils.gemini import generate_json
from app.utils.agno import build_gemini_agent


CRITIC_SYSTEM = (
    "Role: Strict objective critic.\n"
    "Task: Check the assessment JSON is grounded in resume/JD facts and internally consistent (scores align with evidence).\n"
    "If needed, correct scores and text minimally.\n"
    "Output ONLY JSON: { valid: bool, corrected: <assessment>, notes: string[] }."
)


def critique_assessment(assessment: Dict[str, Any], resume_text: str, job_description: str) -> Dict[str, Any]:
    if not settings.gemini_api_key:
        return {"valid": True, "corrected": assessment, "notes": ["LLM not configured; heuristic accepted."]}
    import json
    user = json.dumps({
        "assessment": assessment,
        "resume_text": resume_text[:4000],
        "job_description": job_description[:4000],
    })
    data = None
    agent = build_gemini_agent(CRITIC_SYSTEM)
    if agent is not None:
        try:
            out = agent.run(user)
            text = (out.content or "").strip()
            data = json.loads(text) if text else None
        except Exception:
            data = None
    if not data:
        data = generate_json(CRITIC_SYSTEM, user)
    if not data:
        return {"valid": True, "corrected": assessment, "notes": ["Failed to parse critic output."]}
    return data


