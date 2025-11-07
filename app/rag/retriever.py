from __future__ import annotations

from app.rag.index import vector_index


def retrieve_context(resume_text: str, job_description: str, top_k: int = 5) -> list[str]:
    # Seed the index with JD to bias retrieval
    vector_index.add([job_description])
    results = vector_index.search(query=f"Resume vs JD: {job_description[:256]}", top_k=top_k)
    return results


