import datetime
from uuid import UUID

from sqlalchemy import insert, select, delete
from sqlalchemy.orm import Session

from api.v1.auth.schemas.refresh_session import InRefreshSessionSchema, OutRefreshSessionSchema
from api.v1.auth.models.refresh_session import RefreshSessionModel
from by_objects import ByObject


class RefreshSessionRepository:
    @staticmethod
    def add_refresh_session(db_session: Session, schema: InRefreshSessionSchema) -> OutRefreshSessionSchema:
        stmt = insert(
            RefreshSessionModel
        ).values(
            uuid=schema.uuid,
            user_uuid=schema.user_uuid,
            refresh_token=schema.refresh_token,
            expires_in=schema.expires_in
        ).returning(
            RefreshSessionModel.uuid,
            RefreshSessionModel.user_uuid,
            RefreshSessionModel.refresh_token,
            RefreshSessionModel.expires_in,
        )
        result = db_session.execute(stmt).mappings().one_or_none()
        db_session.commit()
        return OutRefreshSessionSchema(**result)

    @staticmethod
    def get_sessions_by(db_session: Session, by: ByObject) -> list[OutRefreshSessionSchema]:
        query = select(
            RefreshSessionModel.uuid,
            RefreshSessionModel.user_uuid,
            RefreshSessionModel.refresh_token,
            RefreshSessionModel.expires_in,
        ).where(
            by.key.__eq__(by.value)
        )

        result = db_session.execute(query).mappings().fetchall()
        return [OutRefreshSessionSchema(**s) for s in result]

    @staticmethod
    def delete_sessions_by(db_session: Session, by: ByObject) -> None:
        stmt = delete(
            RefreshSessionModel
        ).where(
            by.key.__eq__(by.value)
        )

        db_session.execute(stmt)
        db_session.commit()
