import fitz  # PyMuPDF
import io


def parse_pdf(data: bytes) -> str:
    with fitz.open(stream=io.BytesIO(data), filetype="pdf") as doc:
        texts = []
        for page in doc:
            texts.append(page.get_text())
        return "\n".join(texts).strip()


