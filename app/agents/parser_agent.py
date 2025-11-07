from __future__ import annotations

from typing import Dict, Any
from app.utils.config import settings
from app.utils.gemini import generate_json
from app.utils.agno import build_gemini_agent


SYSTEM_PROMPT = (
    "Role: Expert resume parser.\n"
    "Task: Extract structured JSON with fields: name, title, summary, skills[], experiences[], education[], projects[].\n"
    "- skills: list of strings (normalize casing).\n"
    "- experiences: list of objects { company, role, start_date?, end_date?, duration_months?, responsibilities[], achievements[], relevant_years? }.\n"
    "- education: list of objects { degree, field?, institution, graduation_year? }.\n"
    "Rules: Be concise. Use empty arrays/strings when missing. No prose. Output ONLY JSON."
)


def parse_resume_with_llm(resume_text: str) -> Dict[str, Any]:
    if not settings.gemini_api_key:
        return {
            "name": "",
            "title": "",
            "summary": resume_text[:500],
            "skills": [],
            "experiences": [],
            "education": [],
            "projects": [],
        }

    payload = resume_text[:8000]
    # Prefer Agno Agent
    agent = build_gemini_agent(SYSTEM_PROMPT)
    data = None
    if agent is not None:
        try:
            out = agent.run(payload)
            text = (out.content or "").strip()
            import json
            data = json.loads(text) if text else None
        except Exception:
            data = None
    # Fallback to direct Gemini JSON
    if not data:
        data = generate_json(SYSTEM_PROMPT, payload) or {"summary": payload[:500]}
    return {
        "name": data.get("name", ""),
        "title": data.get("title", ""),
        "summary": data.get("summary", ""),
        "skills": data.get("skills", []),
        "experiences": data.get("experiences", []),
        "education": data.get("education", []),
        "projects": data.get("projects", []),
    }


