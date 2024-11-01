import secrets
from datetime import datetime, timedelta, timezone
from uuid import UUID

from sqlalchemy.orm import Session

from api.v1.auth.models.refresh_session import RefreshSessionModel
from api.v1.auth.schemas.refresh_session import InRefreshSessionSchema, OutRefreshSessionSchema
from api.v1.auth.schemas.token import FingerprintSchema
from api.v1.auth.repositories.refresh_session import RefreshSessionRepository
from api.v1.auth.utils import get_hashed_string
from by_objects import ByToken, ByUUID
from config import settings
from errors import InvalidTokenError


def _generate_refresh_token(fingerprint: FingerprintSchema) -> str:

    str_for_hash = '{user_ip}&{user_agent}&{accept_language}&{token}'.format(
        user_ip=fingerprint.user_ip,
        user_agent=fingerprint.user_agent,
        accept_language=fingerprint.accept_language,
        token=secrets.token_urlsafe(32)
    )
    return get_hashed_string(str_for_hash)


class RefreshSessionService:
    @staticmethod
    def add_session(db_session: Session, user_uuid: UUID, fingerprint: FingerprintSchema) -> OutRefreshSessionSchema:
        schema = InRefreshSessionSchema(
            user_uuid=user_uuid,
            refresh_token=_generate_refresh_token(fingerprint)
        )
        result = RefreshSessionRepository.add_refresh_session(db_session, schema)
        return result

    @staticmethod   
    def get_refresh_sessions_by_user_uuid(db_session: Session, user_uuid: UUID) -> list[OutRefreshSessionSchema]:
        by_uuid = ByUUID(RefreshSessionModel.user_uuid, user_uuid)
        return RefreshSessionRepository.get_sessions_by(db_session, by_uuid)

    @staticmethod
    def get_refresh_session_by_refresh_token(db_session: Session, token: str) -> OutRefreshSessionSchema:
        """
        :except InvalidTokenError
        """
        by_refresh_token = ByToken(RefreshSessionModel.refresh_token, token)
        sessions = RefreshSessionRepository.get_sessions_by(db_session, by_refresh_token)
        if not sessions:
            raise InvalidTokenError
        return sessions[0]

    @staticmethod
    def delete_refresh_session_by_token(db_session: Session, token: str) -> None:
        by_refresh_token = ByToken(RefreshSessionModel.refresh_token, token)
        RefreshSessionRepository.delete_sessions_by(db_session, by_refresh_token)
