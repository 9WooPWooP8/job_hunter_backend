from src.users import service as user_service
from src.users.exceptions import EmailTaken, UsernameTaken
from src.users.schemas import ApplicantCreate, RecruiterCreate


async def valid_applicant_create(user: ApplicantCreate) -> ApplicantCreate:
    existing_user_by_email = await user_service.get_user_by_email(user.email)
    if existing_user_by_email:
        if await user_service.get_applicant_by_id(existing_user_by_email["id"]):
            raise EmailTaken()

    existing_user_by_username = await user_service.get_user_by_username(user.username)
    if existing_user_by_username:
        if await user_service.get_applicant_by_id(existing_user_by_username["id"]):
            raise UsernameTaken()

    return user


async def valid_recruiter_create(user: RecruiterCreate) -> RecruiterCreate:
    existing_user_by_email = await user_service.get_user_by_email(user.email)
    if existing_user_by_email:
        if await user_service.get_recruiter_by_id(existing_user_by_email["id"]):
            raise EmailTaken()

    existing_user_by_username = await user_service.get_user_by_username(user.username)
    if existing_user_by_username:
        if await user_service.get_recruiter_by_id(existing_user_by_username["id"]):
            raise UsernameTaken()

    return user
