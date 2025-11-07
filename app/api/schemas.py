from pydantic import BaseModel, Field
from typing import List, Optional


class AssessmentResponse(BaseModel):
    assessment_id: str
    candidate_name: str | None = None
    candidate_email: str | None = None
    score: float = Field(ge=0, le=100)
    skill_matching_score: float = Field(ge=0, le=100)
    total_experience_matching_score: float = Field(ge=0, le=100)
    relevant_experience_matching_score: float = Field(ge=0, le=100)
    educational_matching_score: float = Field(ge=0, le=100)
    rationale: str
    strengths: List[str] = []
    gaps: List[str] = []
    recommendations: List[str] = []
    objectivity_evidence: List[str] = []


class JobUpsertRequest(BaseModel):
    job_id: str = Field(..., min_length=1, max_length=128)
    job_title: str = Field(..., min_length=2, max_length=256)
    job_description: str = Field(..., min_length=30)


class JobResponse(BaseModel):
    job_id: str
    job_title: str
    job_description: str


class JobSummary(BaseModel):
    id: str
    title: Optional[str] = None


class JobIdsResponse(BaseModel):
    job_ids: List[JobSummary]


class ResumeSummary(BaseModel):
    resume_id: str
    candidate_name: Optional[str] = None
    candidate_email: Optional[str] = None


class AssessmentSummary(BaseModel):
    assessment_id: str
    resume_id: str
    score: float = Field(ge=0, le=100)
    skill_matching_score: float = Field(ge=0, le=100)
    total_experience_matching_score: float = Field(ge=0, le=100)
    relevant_experience_matching_score: float = Field(ge=0, le=100)
    educational_matching_score: float = Field(ge=0, le=100)
    rationale: str
    strengths: List[str] = []
    gaps: List[str] = []
    recommendations: List[str] = []
    objectivity_evidence: List[str] = []




