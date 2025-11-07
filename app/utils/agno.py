from __future__ import annotations

from typing import Optional
from app.utils.config import settings


def build_gemini_agent(system: str):
    try:
        from agno import Agent
        # Try multiple provider paths for compatibility across Agno versions
        try:
            from agno.models.providers.google import Gemini as AgnoGemini  # type: ignore
        except Exception:
            try:
                from agno.models.providers.gemini import Gemini as AgnoGemini  # type: ignore
            except Exception:
                AgnoGemini = None  # type: ignore

        if not settings.gemini_api_key or AgnoGemini is None:
            return None

        llm = AgnoGemini(id=settings.gemini_text_model, api_key=settings.gemini_api_key, temperature=0.2)  # type: ignore
        return Agent(model=llm, system=system)
    except Exception:
        return None


