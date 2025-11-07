from __future__ import annotations

import json
from typing import List, Any
import google.generativeai as genai
from app.utils.config import settings


def _ensure_client() -> None:
    if not settings.gemini_api_key:
        raise RuntimeError("GEMINI_API_KEY not configured")
    genai.configure(api_key=settings.gemini_api_key)


def generate_json(system_prompt: str, user_payload: str) -> dict:
    _ensure_client()
    model = genai.GenerativeModel(model_name=settings.gemini_text_model)
    # For v1beta, pass a simple string; avoid role-based parts
    prompt = f"{system_prompt}\n\n{user_payload}"
    response = model.generate_content(
        prompt,
        generation_config={"response_mime_type": "application/json"},
    )
    # Try multiple ways to extract text
    text = getattr(response, "text", None)
    if not text:
        try:
            text = response.candidates[0].content.parts[0].text  # type: ignore[attr-defined]
        except Exception:
            text = "{}"
    try:
        return json.loads(text)
    except Exception:
        return {}


def _extract_embedding_vector(resp: Any) -> List[float]:
    # Handle multiple response shapes across library versions
    try:
        if isinstance(resp, dict):
            if "embedding" in resp:
                emb = resp["embedding"]
                if isinstance(emb, dict) and "values" in emb:
                    return list(emb["values"])  # type: ignore[list-item]
                if isinstance(emb, list):
                    return list(emb)
            if "embeddings" in resp and isinstance(resp["embeddings"], list):
                first = resp["embeddings"][0]
                if isinstance(first, dict) and "values" in first:
                    return list(first["values"])  # type: ignore[list-item]
        # Object-like
        if hasattr(resp, "embedding"):
            emb = getattr(resp, "embedding")
            if hasattr(emb, "values"):
                return list(getattr(emb, "values"))
            if isinstance(emb, list):
                return list(emb)
        # Direct list
        if isinstance(resp, list) and resp and isinstance(resp[0], (int, float)):
            return list(resp)
    except Exception:
        pass
    return []


def embed_texts(texts: List[str]) -> List[List[float]]:
    _ensure_client()
    model = settings.gemini_embed_model
    vectors: List[List[float]] = []
    for t in texts:
        r = genai.embed_content(model=model, content=t)
        vec = _extract_embedding_vector(r)
        if not vec and isinstance(r, dict) and "embeddings" in r:
            # Batch-like shape fallback
            try:
                vec = _extract_embedding_vector(r["embeddings"][0])  # type: ignore[index]
            except Exception:
                vec = []
        if not vec:
            raise RuntimeError("Failed to extract embedding vector from Gemini response")
        vectors.append(vec)
    return vectors


