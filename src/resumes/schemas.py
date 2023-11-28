from datetime import datetime

from src.models import CustomModel

class EmploymentRecordRequest(CustomModel):
    start_date: datetime
    end_date: datetime
    organization: str
    position: str
    still_working: bool

class ResumeResponse(CustomModel):
    id: int
    applicant_id: int

class ResumeContact(CustomModel):
    contact_id: int
    extra_data: str

class Education(CustomModel):
    education_id: int
    type: str
    end_year: int
    resume_id: int

class ResumeRequest(CustomModel):
    applicant_id: int
    description: str
    job_title: str
    contacts: list[ResumeContact]
    employment_records: list[EmploymentRecordRequest]
    personal_qualities: list[int]
    education: list[Education]

class PersonalQualityResponse(CustomModel):
    id: int
    description: str

class PersonalQualityResponse(CustomModel):
    description:str

class EmploymentRecordResponse(CustomModel):
    id: int
    start_date: datetime
    end_date: datetime
    organization_id: int
    position: str
    resume_id: int