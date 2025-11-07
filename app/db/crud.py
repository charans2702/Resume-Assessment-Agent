from __future__ import annotations

import json
import copy
from sqlalchemy.orm import Session
from app.db.models import Resume, Assessment, Job, ResumeIdentity


def create_resume(db: Session, original_filename: str, content_type: str, text: str) -> Resume:
    resume = Resume(original_filename=original_filename, content_type=content_type, text=text)
    db.add(resume)
    db.flush()
    return resume


def get_resume(db: Session, resume_id: str) -> Resume | None:
    return db.get(Resume, resume_id)


def create_assessment(
    db: Session,
    resume_id: str,
    score: float,
    skill_matching_score: float,
    total_experience_matching_score: float,
    relevant_experience_matching_score: float,
    educational_matching_score: float,
    rationale: str,
    strengths: list[str],
    gaps: list[str],
    recommendations: list[str],
    objectivity_evidence: list[str],
) -> Assessment:
    assessment = Assessment(
        resume_id=resume_id,
        score=score,
        skill_matching_score=skill_matching_score,
        total_experience_matching_score=total_experience_matching_score,
        relevant_experience_matching_score=relevant_experience_matching_score,
        educational_matching_score=educational_matching_score,
        rationale=rationale,
        strengths=json.dumps(strengths),
        gaps=json.dumps(gaps),
        recommendations=json.dumps(recommendations),
        objectivity_evidence=json.dumps(objectivity_evidence),
    )
    db.add(assessment)
    db.flush()
    return assessment


def get_assessment(db: Session, assessment_id: str) -> Assessment | None:
    assessment = db.get(Assessment, assessment_id)
    if not assessment:
        return None
    # hydrate lists
    hydrated = copy.copy(assessment)
    hydrated.strengths = json.loads(assessment.strengths or "[]")
    hydrated.gaps = json.loads(assessment.gaps or "[]")
    hydrated.recommendations = json.loads(assessment.recommendations or "[]")
    hydrated.objectivity_evidence = json.loads(assessment.objectivity_evidence or "[]")
    return hydrated


# Jobs
def upsert_job(db: Session, job_id: str, title: str, description: str) -> Job:
    job = db.get(Job, job_id)
    if job:
        job.title = title
        job.description = description
        db.flush()
        return job
    job = Job(id=job_id, title=title, description=description)
    db.add(job)
    db.flush()
    return job


def get_job(db: Session, job_id: str) -> Job | None:
    return db.get(Job, job_id)


def list_job_ids(db: Session) -> list[str]:
    # Simple select of primary keys
    rows = db.query(Job.id, Job.title).all()
    return [{"id": r.id, "title": r.title} for r in rows]


# Resume identity
def upsert_resume_identity(db: Session, resume_id: str, job_id: str | None, candidate_name: str | None, candidate_email: str | None) -> ResumeIdentity:
    ri = db.get(ResumeIdentity, resume_id)
    if ri:
        # update fields
        ri.job_id = job_id or ri.job_id
        ri.candidate_name = candidate_name or ri.candidate_name
        ri.candidate_email = candidate_email or ri.candidate_email
        db.flush()
        return ri
    ri = ResumeIdentity(resume_id=resume_id, job_id=job_id, candidate_name=candidate_name, candidate_email=candidate_email)
    db.add(ri)
    db.flush()
    return ri


def get_resume_identity(db: Session, resume_id: str) -> ResumeIdentity | None:
    return db.get(ResumeIdentity, resume_id)


def list_resumes_for_job(db: Session, job_id: str) -> list[dict]:
    """
    Return a list of resume metadata for a given job_id:
    [{ resume_id, candidate_name, candidate_email }]
    """
    rows = db.query(ResumeIdentity).filter(ResumeIdentity.job_id == job_id).all()
    return [
        {
            "resume_id": r.resume_id,
            "candidate_name": r.candidate_name,
            "candidate_email": r.candidate_email,
        }
        for r in rows
    ]


def list_assessments_for_resume(db: Session, resume_id: str) -> list[dict]:
    """
    Return hydrated assessments for a resume (lists are JSON-decoded).
    """
    rows = db.query(Assessment).filter(Assessment.resume_id == resume_id).all()
    out = []
    for a in rows:
        hydrated = copy.copy(a)
        hydrated.strengths = json.loads(a.strengths or "[]")
        hydrated.gaps = json.loads(a.gaps or "[]")
        hydrated.recommendations = json.loads(a.recommendations or "[]")
        hydrated.objectivity_evidence = json.loads(a.objectivity_evidence or "[]")
        out.append({
            "assessment_id": hydrated.id,
            "resume_id": hydrated.resume_id,
            "score": hydrated.score,
            "skill_matching_score": hydrated.skill_matching_score,
            "total_experience_matching_score": hydrated.total_experience_matching_score,
            "relevant_experience_matching_score": hydrated.relevant_experience_matching_score,
            "educational_matching_score": hydrated.educational_matching_score,
            "rationale": hydrated.rationale,
            "strengths": hydrated.strengths,
            "gaps": hydrated.gaps,
            "recommendations": hydrated.recommendations,
            "objectivity_evidence": hydrated.objectivity_evidence,
        })
    return out


