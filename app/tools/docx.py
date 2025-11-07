from __future__ import annotations

from docx import Document
import io


def parse_docx(data: bytes) -> str:
    file_like = io.BytesIO(data)
    doc = Document(file_like)
    texts = [p.text.strip() for p in doc.paragraphs if p.text and p.text.strip()]
    return "\n".join(texts)


