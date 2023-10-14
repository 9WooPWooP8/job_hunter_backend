from enum import Enum


class ApplicantStatus(Enum):
    ACTIVELY_LOOKING_FOR_JOB = 1
    ACCEPTING_OFFERS = 2
    NOT_LOOKING_FOR_JOB = 3
