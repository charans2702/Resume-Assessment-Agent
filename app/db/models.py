from sqlalchemy import Column, String, Integer,Float, DateTime, Text, Boolean, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column
import uuid
from app.db.session import Base


def _uuid() -> str:
    return str(uuid.uuid4())


class Resume(Base):
    __tablename__ = "resumes"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    original_filename: Mapped[str] = mapped_column(String(512))
    content_type: Mapped[str] = mapped_column(String(128))
    text: Mapped[str] = mapped_column(Text)


class Assessment(Base):
    __tablename__ = "assessments"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    resume_id: Mapped[str] = mapped_column(String(36))
    score: Mapped[float] = mapped_column(Float)
    skill_matching_score: Mapped[float] = mapped_column(Float, default=0.0)
    total_experience_matching_score: Mapped[float] = mapped_column(Float, default=0.0)
    relevant_experience_matching_score: Mapped[float] = mapped_column(Float, default=0.0)
    educational_matching_score: Mapped[float] = mapped_column(Float, default=0.0)
    rationale: Mapped[str] = mapped_column(Text)
    strengths: Mapped[str] = mapped_column(Text)
    gaps: Mapped[str] = mapped_column(Text)
    recommendations: Mapped[str] = mapped_column(Text)
    objectivity_evidence: Mapped[str] = mapped_column(Text)


class Job(Base):
    __tablename__ = "jobs"
    # Allow client-provided job_id for idempotency across assessments
    id: Mapped[str] = mapped_column(String(128), primary_key=True)
    title: Mapped[str] = mapped_column(String(256))
    description: Mapped[str] = mapped_column(Text)


class ResumeIdentity(Base):
    __tablename__ = "resume_identities"

    resume_id = Column(String, primary_key=True, index=True)
    job_id = Column(String, index=True, nullable=True)

    candidate_name = Column(String, nullable=True)
    candidate_email = Column(String, nullable=True)


