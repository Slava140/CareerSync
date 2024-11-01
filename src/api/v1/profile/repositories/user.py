from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy import insert, select, update
from sqlalchemy.orm import Session

from api.v1.auth.utils import get_hashed_string
from api.v1.profile.models.user import UserModel
from api.v1.profile.schemas.user import InUserSchema, OutUserSchema
from by_objects import ByObject
from database import get_db


class UserRepository:
    @staticmethod
    def is_email_exists(db_session: Session, email: str) -> bool:
        query = select(
            UserModel.email
        ).where(
            UserModel.email == email
        )

        result = db_session.execute(query).one_or_none()

        return bool(result)

    @staticmethod
    def add_user(db_session: Session, schema: InUserSchema) -> OutUserSchema:
        stmt = insert(
            UserModel
        ).values(
            uuid=schema.uuid,
            first_name=schema.first_name,
            middle_name=schema.middle_name,
            last_name=schema.last_name,
            email=schema.email,
            phone_number=schema.phone_number,
            hashed_password=get_hashed_string(schema.password),
            role=schema.role
        ).returning(
            UserModel.uuid,
            UserModel.first_name,
            UserModel.middle_name,
            UserModel.last_name,
            UserModel.email,
            UserModel.phone_number,
            UserModel.role,
            UserModel.created_at,
            UserModel.updated_at,
        )

        result = db_session.execute(stmt).mappings().one_or_none()
        db_session.commit()

        return OutUserSchema(**result)

    @staticmethod
    def get_user_by(db_session: Session, by: ByObject):
        query = select(
            UserModel.uuid,
            UserModel.first_name,
            UserModel.middle_name,
            UserModel.last_name,
            UserModel.email,
            UserModel.phone_number,
            UserModel.role,
            UserModel.created_at,
            UserModel.updated_at
        ).where(
            by.key.__eq__(by.value)
        )

        result = db_session.execute(query).mappings().one_or_none()

        return OutUserSchema(**result) if result is not None else None

    @staticmethod
    def get_password_hash_by_email(db_session: Session, email: str) -> str | None:
        query = select(
            UserModel.hashed_password
        ).where(
            UserModel.email == email
        )

        result = db_session.execute(query).scalar_one_or_none()
        return result

    @staticmethod
    def update_user(db_session: Session, user_uuid: UUID, new_data: dict):
        data = new_data.copy()
        if data.get('password'):
            password = data.pop('password')
            data['hashed_password'] = get_hashed_string(password)
        if data.get('uuid'):
            data.pop('uuid')

        stmt = update(
            UserModel
        ).where(
            UserModel.uuid == str(user_uuid)
        ).values(
            **data
        ).returning(
            UserModel.uuid,
            UserModel.first_name,
            UserModel.middle_name,
            UserModel.last_name,
            UserModel.email,
            UserModel.phone_number,
            UserModel.role,
            UserModel.created_at,
            UserModel.updated_at,
        )

        result = db_session.execute(stmt).mappings().one_or_none()
        return OutUserSchema(**result)


db = next(get_db())
print(UserRepository.get_password_hash_by_email(db, 'user@exaple.com'))
