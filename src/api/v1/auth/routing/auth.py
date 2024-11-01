from fastapi import APIRouter, Request, Response, status
from fastapi.exceptions import HTTPException

from api.v1.auth.schemas.token import FingerprintSchema
from api.v1.auth.services.auth import AuthService
from api.v1.auth.schemas.auth import InLoginSchema, OutLoginSchema, TokensPairSchema
from api.v1.profile.schemas.user import OutUserSchema, InUserSchema
from depends import dbDependency
from errors import (
    InvalidEmailOrPasswordError,
    UserWithUUIDAlreadyHasMaximumRefreshSessionsError,
    InvalidTokenError,
    UserAlreadyExistsError,
)

router = APIRouter(prefix='/auth')


def __add_access_and_refresh_tokens_in_cookie(response: Response, tokens_pair: TokensPairSchema):
    response.set_cookie(
        key='refresh_token', value=tokens_pair.refresh_session.refresh_token,
        httponly=True, expires=tokens_pair.refresh_session.expires_in
    )
    response.set_cookie(
        key='access_token_signature', value=tokens_pair.access_token_signature,
        httponly=True, expires=tokens_pair.access_token_expiration
    )
    response.set_cookie(
        key='access_token', value=tokens_pair.access_token_header_and_payload,
        expires=tokens_pair.access_token_expiration
    )


def __delete_access_and_refresh_tokens_from_cookie(response: Response):
    response.delete_cookie('access_token_signature')
    response.delete_cookie('access_token')
    response.delete_cookie('refresh_token')


@router.post('/login')
def login(
        db_session: dbDependency,
        login_schema: InLoginSchema,
        request: Request,
        response: Response) -> OutUserSchema:

    fingerprint = FingerprintSchema(
        user_ip=request.client.host,
        user_agent=request.headers.get('user-agent'),
        accept_language=request.headers.get('accept-language')
    )
    try:
        login_schema = AuthService.login(db_session, login_schema, fingerprint)
    except InvalidEmailOrPasswordError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
    except UserWithUUIDAlreadyHasMaximumRefreshSessionsError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You already have maximum active sessions")

    refresh_token = request.cookies.get('refresh_token')
    if refresh_token is not None:
        AuthService.logout(db_session, refresh_token)
        __delete_access_and_refresh_tokens_from_cookie(response)

    __add_access_and_refresh_tokens_in_cookie(response, login_schema)

    return login_schema.user


@router.post('/register')
def register(
        db_session: dbDependency,
        user_schema: InUserSchema,
        request: Request,
        response: Response) -> OutUserSchema:

    fingerprint = FingerprintSchema(
        user_ip=request.client.host,
        user_agent=request.headers.get('user-agent'),
        accept_language=request.headers.get('accept-language')
    )
    try:
        login_schema = AuthService.register(db_session, user_schema, fingerprint)
        __add_access_and_refresh_tokens_in_cookie(response, login_schema)
        return login_schema.user
    except UserAlreadyExistsError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists")


@router.post('/logout', status_code=status.HTTP_204_NO_CONTENT)
def logout(db_session: dbDependency, request: Request, response: Response):
    refresh_token = request.cookies.get('refresh_token')
    AuthService.logout(db_session, refresh_token)
    __delete_access_and_refresh_tokens_from_cookie(response)


@router.post('/update-access', status_code=status.HTTP_204_NO_CONTENT)
def update_access(db_session: dbDependency, request: Request, response: Response):
    refresh_token = request.cookies.get('refresh_token')
    if refresh_token is None:
        __delete_access_and_refresh_tokens_from_cookie(response)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token is invalid')

    try:
        new_tokens_pair = AuthService.update_access_token(db_session, refresh_token=refresh_token)
    except InvalidTokenError:
        __delete_access_and_refresh_tokens_from_cookie(response)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token is invalid')

    __add_access_and_refresh_tokens_in_cookie(response, new_tokens_pair)
