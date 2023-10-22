from src.auth.constants import ErrorCode
from src.exceptions import NotAuthenticated, PermissionDenied


class AuthRequired(NotAuthenticated):
    DETAIL = ErrorCode.AUTHENTICATION_REQUIRED


class AuthorizationFailed(PermissionDenied):
    DETAIL = ErrorCode.AUTHORIZATION_FAILED


class InvalidToken(NotAuthenticated):
    DETAIL = ErrorCode.INVALID_TOKEN


class InvalidCredentials(NotAuthenticated):
    DETAIL = ErrorCode.INVALID_CREDENTIALS


class RefreshTokenNotValid(NotAuthenticated):
    DETAIL = ErrorCode.REFRESH_TOKEN_NOT_VALID


class ApplicantNotAuthenticated(NotAuthenticated):
    DETAIL = ErrorCode.APPLICANT_NOT_AUTHENTICATED


class RecruiterNotAuthenticated(NotAuthenticated):
    DETAIL = ErrorCode.RECRUITER_NOT_AUTHENTICATED


class ApplicantNotExists(PermissionDenied):
    DETAIL = ErrorCode.APPLICANT_NOT_EXISTS


class RecruiterNotExists(NotAuthenticated):
    DETAIL = ErrorCode.RECRUITER_NOT_EXISTS
