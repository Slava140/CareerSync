from datetime import datetime, timezone

from sqlalchemy.orm import Session

from api.v1.auth.schemas.auth import InLoginSchema, OutLoginSchema, TokensPairSchema, AccessTokenSchema, \
    FingerprintSchema
from api.v1.auth.services.refresh_session import RefreshSessionService
from api.v1.auth.utils import get_hashed_string, is_correct_hash, generate_access_token
from api.v1.profile.schemas.user import InUserSchema
from api.v1.profile.services.user import UserService

from config import settings
from errors import (
    InvalidEmailOrPasswordError,
    UserWithUUIDAlreadyHasMaximumRefreshSessionsError,
    InvalidTokenError
)


class AuthService:
    @staticmethod
    def __is_login_and_password_valid(db_session, email: str, plain_password: str) -> bool:
        password_hash = UserService.get_password_hash_by_email(db_session, email)
        return is_correct_hash(plain_password, password_hash) if password_hash else False

    @staticmethod
    def login(db_session: Session, schema: InLoginSchema, fingerprint: FingerprintSchema) -> OutLoginSchema:
        """
        :except InvalidEmailOrPasswordError
        :except UserWithUUIDAlreadyHasMaximumRefreshSessionsError
        """
        email = schema.email
        plain_password = schema.password
        if not AuthService.__is_login_and_password_valid(db_session, email, plain_password):
            raise InvalidEmailOrPasswordError

        user = UserService.get_user_by_email(db_session, email)
        user_uuid = user.uuid

        active_user_sessions = RefreshSessionService.get_refresh_sessions_by_user_uuid(db_session, user_uuid)
        if len(active_user_sessions) >= settings.MAX_ACTIVE_USER_SESSIONS_COUNT:
            raise UserWithUUIDAlreadyHasMaximumRefreshSessionsError(user_uuid, settings.MAX_ACTIVE_USER_SESSIONS_COUNT)

        access_token_payload = AccessTokenSchema(sub=user_uuid)
        access_token = generate_access_token(access_token_payload)
        header_and_payload, signature = access_token.rsplit('.', maxsplit=1)
        refresh_session = RefreshSessionService.add_session(
            db_session=db_session,
            user_uuid=user_uuid,
            fingerprint=fingerprint
        )

        return OutLoginSchema(
            access_token_header_and_payload=header_and_payload,
            access_token_signature=signature,
            access_token_expiration=access_token_payload.exp,
            refresh_session=refresh_session,
            user=user
        )

    @staticmethod
    def register(db_session: Session, user_schema: InUserSchema, fingerprint: FingerprintSchema) -> OutLoginSchema:
        """
        :except UserAlreadyExistsError
        """
        created_user = UserService.add_user(db_session, user_schema)
        login_schema = InLoginSchema(email=created_user.email, password=user_schema.password)
        return AuthService.login(db_session, login_schema, fingerprint)

    @staticmethod
    def logout(db_session: Session, refresh_token: str) -> None:
        RefreshSessionService.delete_refresh_session_by_token(db_session, refresh_token)

    @staticmethod
    def update_access_token(db_session: Session, refresh_token: str) -> TokensPairSchema:
        refresh_session = RefreshSessionService.get_refresh_session_by_refresh_token(db_session, refresh_token)
        if refresh_session.expires_in <= datetime.now(timezone.utc):
            raise InvalidTokenError
        access_token_payload = AccessTokenSchema(sub=refresh_session.user_uuid)
        new_access_token = generate_access_token(access_token_payload)
        header_and_payload, signature = new_access_token.rsplit('.', maxsplit=1)
        return TokensPairSchema(
            refresh_session=refresh_session,
            access_token_header_and_payload=header_and_payload,
            access_token_signature=signature,
            access_token_expiration=access_token_payload.exp
        )

    @staticmethod
    def get_user(db_session: Session):
        ...
