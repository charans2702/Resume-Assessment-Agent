from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi import Depends
from app.api.schemas import (
    AssessmentResponse,
    JobUpsertRequest,
    JobResponse,
    JobIdsResponse,
    ResumeSummary,
    AssessmentSummary,
)
from app.db import crud
from app.db.session import get_db
from sqlalchemy.orm import Session
from app.tools.pdf import parse_pdf
from app.tools.text import parse_text
from app.tools.ocr import parse_image
from app.tools.docx import parse_docx
from app.agents.orchestrator import run_assessment_pipeline

router = APIRouter()



@router.post("/jobs", response_model=JobResponse)
async def upsert_job(request: JobUpsertRequest, db: Session = Depends(get_db)):
    job = crud.upsert_job(db, job_id=request.job_id, title=request.job_title, description=request.job_description)
    return JobResponse(job_id=job.id, job_title=job.title, job_description=job.description)


@router.get("/jobs", response_model=JobIdsResponse)
async def list_jobs(db: Session = Depends(get_db)):
    ids = crud.list_job_ids(db)
    return JobIdsResponse(job_ids=ids)


@router.post("/jobs/{job_id}/assess", response_model=AssessmentResponse)
async def assess_for_job(job_id: str, file: UploadFile = File(...), db: Session = Depends(get_db)):
    job = crud.get_job(db, job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    content_type = file.content_type or "application/octet-stream"
    data = await file.read()

    try:
        if content_type in ("application/pdf",):
            text = parse_pdf(data)
        elif content_type in ("application/vnd.openxmlformats-officedocument.wordprocessingml.document",):
            text = parse_docx(data)
        elif content_type.startswith("text/"):
            text = parse_text(data)
        elif content_type.startswith("image/"):
            text = parse_image(data)
        else:
            # Try by filename extension as a fallback for some clients
            name = (file.filename or "").lower()
            if name.endswith(".pdf"):
                text = parse_pdf(data)
            elif name.endswith(".docx"):
                text = parse_docx(data)
            elif name.endswith(".txt"):
                text = parse_text(data)
            else:
                raise HTTPException(status_code=400, detail=f"Unsupported content type: {content_type}")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to parse resume: {e}")

    resume = crud.create_resume(db, original_filename=file.filename, content_type=content_type, text=text)
    assessment = run_assessment_pipeline(db=db, job_id=job_id, resume_id=resume.id, resume_text=resume.text, job_description=job.description)
    return AssessmentResponse(**assessment)


@router.get("/jobs/{job_id}/resumes", response_model=list[ResumeSummary])
async def list_resumes_for_job(job_id: str, db: Session = Depends(get_db)):
    """
    Return list of resumes for a job id with resume_id, candidate_name, candidate_email.
    Uses: app/db/crud.py -> list_resumes_for_job
    """
    rows = crud.list_resumes_for_job(db, job_id)
    return [ResumeSummary(resume_id=r["resume_id"], candidate_name=r.get("candidate_name"), candidate_email=r.get("candidate_email")) for r in rows]


@router.get("/resumes/{resume_id}/assessments", response_model=list[AssessmentSummary])
async def list_assessments_for_resume(resume_id: str, db: Session = Depends(get_db)):
    """
    Return hydrated assessments for a resume id.
    Uses: app/db/crud.py -> list_assessments_for_resume
    """
    rows = crud.list_assessments_for_resume(db, resume_id)
    # rows already contain the expected fields
    return rows


