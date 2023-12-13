from datetime import datetime

from src.models import CustomModel


class EmploymentRecordRequest(CustomModel):
    id: int | None = None
    start_date: datetime
    end_date: datetime
    organization: str
    position: str
    still_working: bool

class ResumeContact(CustomModel):
    contact_id: int
    extra_data: str


class Education(CustomModel):
    id: int
    type: str


class ResumeEducationRequest(CustomModel):
    education_id: int
    end_year: int


class ResumeEducationResponse(CustomModel):
    education_id: int
    end_year: int
    education: Education


class PersonalQualityResponse(CustomModel):
    id: int
    description: str

class StatusResponse(CustomModel):
    id: int
    status: str

class ResumeResponse(CustomModel):
    id: int
    applicant_id: int
    photo: str | None
    job_title: str
    description: str
    created_at: datetime
    contacts: list[ResumeContact]
    employment_records: list[EmploymentRecordRequest]
    personal_qualities: str | None
    educations: list[ResumeEducationResponse]
    status: StatusResponse


class ResumeRequest(CustomModel):
    applicant_id: int
    description: str
    job_title: str
    contacts: list[ResumeContact]
    employment_records: list[EmploymentRecordRequest]
    personal_qualities: str | None
    education: list[ResumeEducationRequest]
    status: int


class EmploymentRecordResponse(CustomModel):
    id: int
    start_date: datetime
    end_date: datetime
    organization_id: int
    position: str
    resume_id: int
