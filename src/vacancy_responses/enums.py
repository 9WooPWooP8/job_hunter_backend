from enum import Enum


class VacancyResponseStatusEnum(Enum):
    WAITING_FOR_REVIEW = 1
    REVIEWED = 2
    DECLINED = 3
