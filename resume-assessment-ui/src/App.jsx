import React, { useState, useEffect } from 'react';
import { Upload, Briefcase, FileText, TrendingUp, Award, AlertCircle, CheckCircle, ArrowLeft, Plus, X } from 'lucide-react';

// API Configuration - Update this with your backend URL
const API_BASE_URL = 'http://localhost:8000/v1';

const styles = `
  * {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
  }

  body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', sans-serif;
    -webkit-font-smoothing: antialiased;
  }

  .app-container {
    min-height: 100vh;
    background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
  }

  .header {
    background: white;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    border-bottom: 1px solid #e2e8f0;
  }

  .header-content {
    max-width: 1280px;
    margin: 0 auto;
    padding: 1rem 1.5rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
  }

  .header-left {
    display: flex;
    align-items: center;
    gap: 0.75rem;
  }

  .logo {
    background: #2563eb;
    padding: 0.5rem;
    border-radius: 0.5rem;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .logo svg {
    width: 1.5rem;
    height: 1.5rem;
    color: white;
  }

  .header-title h1 {
    font-size: 1.5rem;
    font-weight: bold;
    color: #0f172a;
  }

  .header-title p {
    font-size: 0.875rem;
    color: #64748b;
  }

  .btn {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.5rem 1rem;
    border-radius: 0.5rem;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s;
    border: none;
    font-size: 0.875rem;
  }

  .btn-primary {
    background: #2563eb;
    color: white;
  }

  .btn-primary:hover {
    background: #1d4ed8;
  }

  .btn-secondary {
    background: transparent;
    border: 1px solid #cbd5e1;
    color: #475569;
  }

  .btn-secondary:hover {
    background: #f8fafc;
  }

  .btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }

  .main-content {
    max-width: 1280px;
    margin: 0 auto;
    padding: 2rem 1.5rem;
  }

  .error-banner {
    background: #fef2f2;
    border: 1px solid #fecaca;
    color: #991b1b;
    padding: 1rem;
    border-radius: 0.5rem;
    margin-bottom: 1.5rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }

  .error-banner button {
    margin-left: auto;
    background: none;
    border: none;
    cursor: pointer;
    color: #991b1b;
  }

  .section-header {
    margin-bottom: 1.5rem;
  }

  .section-header h2 {
    font-size: 1.25rem;
    font-weight: 600;
    color: #0f172a;
  }

  .section-header p {
    color: #475569;
    margin-top: 0.25rem;
  }

  .loading {
    text-align: center;
    padding: 3rem 0;
  }

  .spinner {
    display: inline-block;
    width: 3rem;
    height: 3rem;
    border: 3px solid #e2e8f0;
    border-top-color: #2563eb;
    border-radius: 50%;
    animation: spin 1s linear infinite;
  }

  @keyframes spin {
    to { transform: rotate(360deg); }
  }

  .grid {
    display: grid;
    gap: 1rem;
  }

  .grid-cols-3 {
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  }

  .grid-cols-2 {
    grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  }

  .grid-cols-4 {
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  }

  .card {
    background: white;
    padding: 1.5rem;
    border-radius: 0.75rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    border: 1px solid #e2e8f0;
    transition: all 0.2s;
  }

  .card-clickable {
    cursor: pointer;
  }

  .card-clickable:hover {
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    border-color: #93c5fd;
  }

  .card-header {
    display: flex;
    align-items: start;
    gap: 0.75rem;
  }

  .icon-box {
    padding: 0.5rem;
    border-radius: 0.5rem;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .icon-box svg {
    width: 1.25rem;
    height: 1.25rem;
  }

  .icon-blue {
    background: #dbeafe;
    color: #2563eb;
  }

  .icon-green {
    background: #dcfce7;
    color: #16a34a;
  }

  .card-content {
    flex: 1;
  }

  .card-content h3 {
    font-weight: 600;
    color: #0f172a;
    margin-bottom: 0.25rem;
  }

  .card-content p {
    font-size: 0.875rem;
    color: #64748b;
    margin-top: 0.25rem;
  }

  .card-content .small {
    font-size: 0.75rem;
    color: #94a3b8;
  }

  .empty-state {
    text-align: center;
    padding: 3rem 0;
    background: white;
    border-radius: 0.75rem;
    border: 1px solid #e2e8f0;
  }

  .empty-state svg {
    width: 3rem;
    height: 3rem;
    color: #cbd5e1;
    margin: 0 auto 0.75rem;
  }

  .empty-state p {
    color: #475569;
  }

  .back-btn {
    display: flex;
    align-items: center;
    gap: 0.25rem;
    color: #475569;
    background: none;
    border: none;
    cursor: pointer;
    font-size: 0.875rem;
    margin-bottom: 1rem;
  }

  .back-btn:hover {
    color: #0f172a;
  }

  .resumes-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 1.5rem;
  }

  .resumes-header-left {
    display: flex;
    align-items: center;
    gap: 1rem;
  }

  .score-hero {
    background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
    padding: 1.5rem;
    border-radius: 0.75rem;
    color: white;
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 1.5rem;
  }

  .score-hero-left p:first-child {
    color: #bfdbfe;
    font-size: 0.875rem;
  }

  .score-hero-left p:last-child {
    font-size: 3rem;
    font-weight: bold;
    margin-top: 0.5rem;
  }

  .score-hero svg {
    width: 4rem;
    height: 4rem;
    color: #93c5fd;
  }

  .score-card {
    background: white;
    padding: 1rem;
    border-radius: 0.75rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    border: 1px solid #e2e8f0;
  }

  .score-card-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 0.5rem;
  }

  .score-card-header span {
    font-size: 0.875rem;
    color: #475569;
  }

  .score-card-icon {
    padding: 0.375rem;
    border-radius: 0.5rem;
  }

  .score-card-icon svg {
    width: 1.25rem;
    height: 1.25rem;
  }

  .score-high {
    background: #dcfce7;
    color: #16a34a;
  }

  .score-medium {
    background: #fef3c7;
    color: #ca8a04;
  }

  .score-low {
    background: #fee2e2;
    color: #dc2626;
  }

  .score-card p {
    font-size: 1.875rem;
    font-weight: bold;
    color: #0f172a;
  }

  .info-card {
    padding: 1.5rem;
    border-radius: 0.75rem;
    border: 1px solid;
  }

  .info-card-green {
    background: #f0fdf4;
    border-color: #bbf7d0;
  }

  .info-card-orange {
    background: #fff7ed;
    border-color: #fed7aa;
  }

  .info-card-blue {
    background: #eff6ff;
    border-color: #bfdbfe;
  }

  .info-card h3 {
    font-weight: 600;
    color: #0f172a;
    margin-bottom: 0.75rem;
  }

  .info-card ul {
    list-style: none;
  }

  .info-card li {
    display: flex;
    align-items: start;
    gap: 0.5rem;
    margin-bottom: 0.5rem;
  }

  .info-card li span:first-child {
    color: #94a3b8;
  }

  .info-card li span:last-child {
    color: #334155;
    font-size: 0.875rem;
  }

  .info-card .empty {
    color: #64748b;
    font-size: 0.875rem;
  }

  .rationale-card {
    background: white;
    padding: 1.5rem;
    border-radius: 0.75rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    border: 1px solid #e2e8f0;
    margin-bottom: 1.5rem;
  }

  .rationale-card h3 {
    font-weight: 600;
    color: #0f172a;
    margin-bottom: 0.75rem;
  }

  .rationale-card p {
    color: #334155;
    line-height: 1.6;
  }

  .evidence-card {
    background: white;
    padding: 1.5rem;
    border-radius: 0.75rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    border: 1px solid #e2e8f0;
  }

  .evidence-card h3 {
    font-weight: 600;
    color: #0f172a;
    margin-bottom: 0.75rem;
  }

  .evidence-card ul {
    list-style: none;
  }

  .evidence-card li {
    display: flex;
    align-items: start;
    gap: 0.5rem;
    margin-bottom: 0.5rem;
  }

  .evidence-card li svg {
    width: 1.25rem;
    height: 1.25rem;
    color: #16a34a;
    flex-shrink: 0;
    margin-top: 0.125rem;
  }

  .evidence-card li span {
    color: #334155;
  }

  .modal-overlay {
    position: fixed;
    inset: 0;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 1rem;
    z-index: 50;
  }

  .modal {
    background: white;
    border-radius: 0.75rem;
    box-shadow: 0 20px 25px rgba(0,0,0,0.15);
    width: 100%;
    max-height: 90vh;
    overflow-y: auto;
  }

  .modal-small {
    max-width: 28rem;
  }

  .modal-large {
    max-width: 42rem;
  }

  .modal-header {
    padding: 1.5rem;
    border-bottom: 1px solid #e2e8f0;
    display: flex;
    align-items: center;
    justify-content: space-between;
  }

  .modal-header h2 {
    font-size: 1.25rem;
    font-weight: bold;
    color: #0f172a;
  }

  .modal-header button {
    background: none;
    border: none;
    color: #94a3b8;
    cursor: pointer;
  }

  .modal-header button:hover {
    color: #475569;
  }

  .modal-header svg {
    width: 1.5rem;
    height: 1.5rem;
  }

  .modal-body {
    padding: 1.5rem;
  }

  .form-group {
    margin-bottom: 1rem;
  }

  .form-label {
    display: block;
    font-size: 0.875rem;
    font-weight: 500;
    color: #334155;
    margin-bottom: 0.5rem;
  }

  .form-input {
    width: 100%;
    padding: 0.5rem 1rem;
    border: 1px solid #cbd5e1;
    border-radius: 0.5rem;
    font-size: 0.875rem;
  }

  .form-input:focus {
    outline: none;
    border-color: #2563eb;
    box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
  }

  .form-textarea {
    width: 100%;
    padding: 0.5rem 1rem;
    border: 1px solid #cbd5e1;
    border-radius: 0.5rem;
    font-size: 0.875rem;
    resize: vertical;
    font-family: inherit;
  }

  .form-textarea:focus {
    outline: none;
    border-color: #2563eb;
    box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
  }

  .form-actions {
    display: flex;
    gap: 0.75rem;
    padding-top: 1rem;
  }

  .form-actions button {
    flex: 1;
  }

  .upload-area {
    border: 2px dashed #cbd5e1;
    border-radius: 0.5rem;
    padding: 2rem;
    text-align: center;
    transition: border-color 0.2s;
  }

  .upload-area:hover {
    border-color: #60a5fa;
  }

  .upload-area svg {
    width: 3rem;
    height: 3rem;
    color: #cbd5e1;
    margin: 0 auto 0.75rem;
  }

  .upload-area label {
    cursor: pointer;
  }

  .upload-area label span {
    color: #2563eb;
    font-weight: 500;
  }

  .upload-area label span:hover {
    color: #1d4ed8;
  }

  .upload-area input {
    display: none;
  }

  .upload-area .hint {
    font-size: 0.875rem;
    color: #64748b;
    margin-top: 0.5rem;
  }

  .upload-area .filename {
    font-size: 0.875rem;
    color: #16a34a;
    font-weight: 500;
    margin-top: 0.75rem;
  }

  @media (max-width: 768px) {
    .header-content {
      flex-direction: column;
      gap: 1rem;
      align-items: flex-start;
    }

    .grid-cols-3,
    .grid-cols-2,
    .grid-cols-4 {
      grid-template-columns: 1fr;
    }

    .score-hero {
      flex-direction: column;
      gap: 1rem;
    }

    .score-hero svg {
      width: 3rem;
      height: 3rem;
    }

    .resumes-header {
      flex-direction: column;
      align-items: flex-start;
      gap: 1rem;
    }
  }
`;

const App = () => {
  const [view, setView] = useState('jobs');
  const [jobs, setJobs] = useState([]);
  const [selectedJob, setSelectedJob] = useState(null);
  const [resumes, setResumes] = useState([]);
  const [selectedResume, setSelectedResume] = useState(null);
  const [assessments, setAssessments] = useState([]);
  const [loading, setLoading] = useState(false);
  const [showCreateJob, setShowCreateJob] = useState(false);
  const [showUploadResume, setShowUploadResume] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchJobs();
  }, []);

  const fetchJobs = async () => {
    try {
      setLoading(true);
      const response = await fetch(`${API_BASE_URL}/jobs`);
      const data = await response.json();
      setJobs(data.job_ids || []);
    } catch (err) {
      setError('Failed to fetch jobs');
    } finally {
      setLoading(false);
    }
  };

  const fetchResumesForJob = async (jobId) => {
    try {
      setLoading(true);
      const response = await fetch(`${API_BASE_URL}/jobs/${jobId}/resumes`);
      const data = await response.json();
      setResumes(data);
    } catch (err) {
      setError('Failed to fetch resumes');
    } finally {
      setLoading(false);
    }
  };

  const fetchAssessmentsForResume = async (resumeId) => {
    try {
      setLoading(true);
      const response = await fetch(`${API_BASE_URL}/resumes/${resumeId}/assessments`);
      const data = await response.json();
      setAssessments(data);
    } catch (err) {
      setError('Failed to fetch assessments');
    } finally {
      setLoading(false);
    }
  };

  const handleJobClick = async (job) => {
    setSelectedJob(job);
    setView('resumes');
    await fetchResumesForJob(job.id);
  };

  const handleResumeClick = async (resume) => {
    setSelectedResume(resume);
    setView('assessment');
    await fetchAssessmentsForResume(resume.resume_id);
  };

  const handleBackToJobs = () => {
    setView('jobs');
    setSelectedJob(null);
    setResumes([]);
  };

  const handleBackToResumes = () => {
    setView('resumes');
    setSelectedResume(null);
    setAssessments([]);
  };

  return (
    <>
      <style>{styles}</style>
      <div className="app-container">
        <header className="header">
          <div className="header-content">
            <div className="header-left">
              <div className="logo">
                <Briefcase />
              </div>
              <div className="header-title">
                <h1>Resume Assessment System</h1>
                <p>AI-Powered Candidate Evaluation</p>
              </div>
            </div>
            {view === 'jobs' && (
              <button onClick={() => setShowCreateJob(true)} className="btn btn-primary">
                <Plus />
                <span>New Job</span>
              </button>
            )}
          </div>
        </header>

        <main className="main-content">
          {error && (
            <div className="error-banner">
              <AlertCircle />
              {error}
              <button onClick={() => setError(null)}>
                <X />
              </button>
            </div>
          )}

          {view === 'jobs' && (
            <div>
              <div className="section-header">
                <h2>All Job Positions</h2>
                <p>Select a job to view candidate assessments</p>
              </div>
              {loading ? (
                <div className="loading">
                  <div className="spinner"></div>
                </div>
              ) : (
                <div className="grid grid-cols-3">
                  {jobs.map((job) => (
                    <div key={job.id} onClick={() => handleJobClick(job)} className="card card-clickable">
                      <div className="card-header">
                        <div className="icon-box icon-blue">
                          <Briefcase />
                        </div>
                        <div className="card-content">
                          <h3>{job.title || 'Untitled Position'}</h3>
                          <p className="small">Job ID: {job.id}</p>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}

          {view === 'resumes' && (
            <div>
              <div className="resumes-header">
                <div className="resumes-header-left">
                  <button onClick={handleBackToJobs} className="back-btn">
                    <ArrowLeft />
                    Back
                  </button>
                  <div>
                    <h2 className="section-header">{selectedJob?.title}</h2>
                    <p>Candidate Resumes</p>
                  </div>
                </div>
                <button onClick={() => setShowUploadResume(true)} className="btn btn-primary">
                  <Upload />
                  <span>Upload Resume</span>
                </button>
              </div>
              {loading ? (
                <div className="loading">
                  <div className="spinner"></div>
                </div>
              ) : resumes.length === 0 ? (
                <div className="empty-state">
                  <FileText />
                  <p>No resumes assessed for this job yet</p>
                </div>
              ) : (
                <div className="grid grid-cols-2">
                  {resumes.map((resume) => (
                    <div key={resume.resume_id} onClick={() => handleResumeClick(resume)} className="card card-clickable">
                      <div className="card-header">
                        <div className="icon-box icon-green">
                          <FileText />
                        </div>
                        <div className="card-content">
                          <h3>{resume.candidate_name || 'Anonymous Candidate'}</h3>
                          <p>{resume.candidate_email || 'No email provided'}</p>
                          <p className="small">ID: {resume.resume_id}</p>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}

          {view === 'assessment' && assessments.length > 0 && (
            <div>
              <button onClick={handleBackToResumes} className="back-btn">
                <ArrowLeft />
                Back to Resumes
              </button>
              <div className="card" style={{ marginBottom: '1.5rem' }}>
                <h2 style={{ fontSize: '1.5rem', fontWeight: 'bold', color: '#0f172a' }}>
                  {selectedResume?.candidate_name || 'Candidate Assessment'}
                </h2>
                <p style={{ color: '#475569', marginTop: '0.25rem' }}>{selectedResume?.candidate_email}</p>
              </div>

              {assessments.map((assessment) => (
                <div key={assessment.assessment_id}>
                  <div className="score-hero">
                    <div className="score-hero-left">
                      <p>Overall Match Score</p>
                      <p>{assessment.score.toFixed(1)}%</p>
                    </div>
                    <Award />
                  </div>

                  <div className="grid grid-cols-4" style={{ marginBottom: '1.5rem' }}>
                    <ScoreCard title="Skills Match" score={assessment.skill_matching_score} icon={<TrendingUp />} />
                    <ScoreCard title="Total Experience" score={assessment.total_experience_matching_score} icon={<Briefcase />} />
                    <ScoreCard title="Relevant Experience" score={assessment.relevant_experience_matching_score} icon={<CheckCircle />} />
                    <ScoreCard title="Education" score={assessment.educational_matching_score} icon={<Award />} />
                  </div>

                  <div className="rationale-card">
                    <h3>Assessment Rationale</h3>
                    <p>{assessment.rationale}</p>
                  </div>

                  <div className="grid grid-cols-3" style={{ marginBottom: '1.5rem' }}>
                    <InfoCard title="Strengths" items={assessment.strengths} color="green" />
                    <InfoCard title="Gaps" items={assessment.gaps} color="orange" />
                    <InfoCard title="Recommendations" items={assessment.recommendations} color="blue" />
                  </div>

                  {assessment.objectivity_evidence.length > 0 && (
                    <div className="evidence-card">
                      <h3>Objectivity Evidence</h3>
                      <ul>
                        {assessment.objectivity_evidence.map((item, idx) => (
                          <li key={idx}>
                            <CheckCircle />
                            <span>{item}</span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}
        </main>

        {showCreateJob && (
          <CreateJobModal onClose={() => setShowCreateJob(false)} onSuccess={fetchJobs} />
        )}

        {showUploadResume && selectedJob && (
          <UploadResumeModal
            jobId={selectedJob.id}
            onClose={() => setShowUploadResume(false)}
            onSuccess={() => fetchResumesForJob(selectedJob.id)}
          />
        )}
      </div>
    </>
  );
};

const ScoreCard = ({ title, score, icon }) => {
  const getScoreClass = (score) => {
    if (score >= 75) return 'score-high';
    if (score >= 50) return 'score-medium';
    return 'score-low';
  };

  return (
    <div className="score-card">
      <div className="score-card-header">
        <span>{title}</span>
        <div className={`score-card-icon ${getScoreClass(score)}`}>{icon}</div>
      </div>
      <p>{score.toFixed(1)}%</p>
    </div>
  );
};

const InfoCard = ({ title, items, color }) => {
  return (
    <div className={`info-card info-card-${color}`}>
      <h3>{title}</h3>
      {items.length === 0 ? (
        <p className="empty">None identified</p>
      ) : (
        <ul>
          {items.map((item, idx) => (
            <li key={idx}>
              <span>•</span>
              <span>{item}</span>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

const CreateJobModal = ({ onClose, onSuccess }) => {
  const [formData, setFormData] = useState({
    job_id: '',
    job_title: '',
    job_description: '',
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const response = await fetch(`${API_BASE_URL}/jobs`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData),
      });

      if (!response.ok) throw new Error('Failed to create job');

      onSuccess();
      onClose();
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="modal-overlay">
      <div className="modal modal-large">
        <div className="modal-header">
          <h2>Create New Job</h2>
          <button onClick={onClose}>
            <X />
          </button>
        </div>
        <form onSubmit={handleSubmit} className="modal-body">
          {error && (
            <div className="error-banner">
              {error}
            </div>
          )}
          <div className="form-group">
            <label className="form-label">Job ID</label>
            <input
              type="text"
              required
              value={formData.job_id}
              onChange={(e) => setFormData({ ...formData, job_id: e.target.value })}
              className="form-input"
              placeholder="e.g., SWE-2024-001"
            />
          </div>
          <div className="form-group">
            <label className="form-label">Job Title</label>
            <input
              type="text"
              required
              value={formData.job_title}
              onChange={(e) => setFormData({ ...formData, job_title: e.target.value })}
              className="form-input"
              placeholder="e.g., Senior Software Engineer"
            />
          </div>
          <div className="form-group">
            <label className="form-label">Job Description</label>
            <textarea
              required
              rows={6}
              value={formData.job_description}
              onChange={(e) => setFormData({ ...formData, job_description: e.target.value })}
              className="form-textarea"
              placeholder="Paste the full job description here..."
            />
          </div>
          <div className="form-actions">
            <button type="button" onClick={onClose} className="btn btn-secondary">
              Cancel
            </button>
            <button type="submit" disabled={loading} className="btn btn-primary">
              {loading ? 'Creating...' : 'Create Job'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

const UploadResumeModal = ({ jobId, onClose, onSuccess }) => {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) return;

    setLoading(true);
    setError(null);

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch(`${API_BASE_URL}/jobs/${jobId}/assess`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) throw new Error('Failed to upload and assess resume');

      onSuccess();
      onClose();
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="modal-overlay">
      <div className="modal modal-small">
        <div className="modal-header">
          <h2>Upload Resume</h2>
          <button onClick={onClose}>
            <X />
          </button>
        </div>
        <form onSubmit={handleSubmit} className="modal-body">
          {error && (
            <div className="error-banner" style={{ fontSize: '0.875rem' }}>
              {error}
            </div>
          )}
          <div className="upload-area">
            <Upload />
            <label>
              <span>Choose a file</span>
              <input
                type="file"
                accept=".pdf,.docx,.txt,image/*"
                onChange={(e) => setFile(e.target.files[0])}
              />
            </label>
            <p className="hint">PDF, DOCX, TXT, or Image files</p>
            {file && (
              <p className="filename">{file.name}</p>
            )}
          </div>
          <div className="form-actions">
            <button type="button" onClick={onClose} className="btn btn-secondary">
              Cancel
            </button>
            <button type="submit" disabled={!file || loading} className="btn btn-primary">
              {loading ? 'Analyzing...' : 'Upload & Assess'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default App;