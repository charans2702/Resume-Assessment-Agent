# Resume Assessment Agent 

A FastAPI-based agent pipeline that ingests resumes (PDF, text, image), parses them, compares them against a provided Job Description (JD), and returns an objective assessment with rationale. Uses Google Gemini (via direct SDK or Agno), local RAG with FAISS, and SQLite storage. A browser UI is included under `resume-assessment-ui/`.


Features
- Multi-agent pipeline: parsing, assessment, critique, and orchestration via [`run_assessment_pipeline`](app/agents/orchestrator.py).
- File parsing tools: PDF ([`app.tools.pdf.parse_pdf`](app/tools/pdf.py)), DOCX ([`app.tools.docx.parse_docx`](app/tools/docx.py)), plain text ([`app.tools.text.parse_text`](app/tools/text.py)), and OCR ([`app.tools.ocr.parse_image`](app/tools/ocr.py)).
- Local vector store using FAISS with Gemini embeddings ([`app.rag.index.VectorIndex`](app/rag/index.py)).
- SQLite-backed persistence and simple CRUD utilities ([`app.db.crud`](app/db/crud.py)).
- Guardrails: PII scrub and schema validation ([`app.guardrails.validators`](app/guardrails/validators.py)).

Requirements
- Python 3.10+
- System: Tesseract OCR (for image parsing), MuPDF/Poppler (for PDF parsing)
- Node.js & npm (for the UI)
- See [requirements.txt](requirements.txt)

Configuration
Create a `.env` in the project root with at least:
- GEMINI_API_KEY (or set in environment)
- GEMINI_TEXT_MODEL (optional)
- GEMINI_EMBED_MODEL (optional)
- DATABASE_URL (optional; default: sqlite:///./data/app.db)
- VECTOR_INDEX_PATH (optional; default: ./data/index.faiss)

The app uses [`app.utils.config.settings`](app/utils/config.py) to read these values.


Quickstart — Backend
1. Create virtualenv and install:
```bash
# from project root
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Prepare environment:
```bash
cp .env.example .env  # if present, or create .env manually
# export GEMINI_API_KEY=your_key
# export DATABASE_URL=sqlite:///./data/app.db
```

3. Run the API (development):
```bash
uvicorn app.main:app --reload
```
This boots the FastAPI app created by [`app.main.create_app`](app/main.py).

Quickstart — UI
The UI is in the `resume-assessment-ui/` folder. Typical steps (Vite-based):
```bash
cd resume-assessment-ui
npm install
npm run dev      # start development server (usually :5173)
# or build:
npm run build
npm run preview
```
Files of interest: [resume-assessment-ui/package.json](resume-assessment-ui/package.json), [resume-assessment-ui/index.html](resume-assessment-ui/index.html), and [resume-assessment-ui/src/](resume-assessment-ui/src/).

How the API is used by the UI
Primary endpoints (implemented in [app/api/routes.py](app/api/routes.py)):
- POST /v1/jobs — upsert a job. Handler: [`upsert_job`](app/api/routes.py).
- GET /v1/jobs — list job ids. Handler: [`list_jobs`](app/api/routes.py).
- POST /v1/jobs/{job_id}/assess — upload a resume file (pdf/docx/txt/image) to assess. Handler: [`assess_for_job`](app/api/routes.py).
- GET /v1/jobs/{job_id}/resumes — list resumes linked to a job.
- GET /v1/resumes/{resume_id}/assessments — list assessments for a resume.

Storage & Index
- DB: the app initializes the DB and tables via [`app.db.session.init_engine_and_create`](app/db/session.py).
- Vector index: persisted at `VECTOR_INDEX_PATH` (default `./data/index.faiss`) handled by [`app.rag.index.VectorIndex`](app/rag/index.py).

Troubleshooting
- PDF parsing requires MuPDF/PyMuPDF: ensure libmupdf is available on the system.
- OCR requires Tesseract installed and on PATH.
- FAISS installation can be platform-sensitive; the project uses `faiss-cpu` in requirements.

Extending / Notes for Developers
- Gemini integration is in [`app/utils/gemini.py`](app/utils/gemini.py) and optionally wrapped via Agno in [`app.utils.agno.build_gemini_agent`](app/utils/agno.py).
- Agents follow a simple pattern: parse -> assess -> critique -> guardrails. Core orchestrator: [`app.agents.orchestrator.run_assessment_pipeline`](app/agents/orchestrator.py).
- Data model and persistence: [app/db/models.py](app/db/models.py) and [app/db/crud.py](app/db/crud.py).




