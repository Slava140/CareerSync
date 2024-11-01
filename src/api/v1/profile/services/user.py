from uuid import UUID

from sqlalchemy.orm import Session

from api.v1.profile.models.user import UserModel
from api.v1.profile.repositories.user import UserRepository
from api.v1.profile.schemas.user import OutUserSchema, InUserSchema
from by_objects import ByEmail, ByUUID
from errors import UserAlreadyExistsError


class UserService:
    @staticmethod
    def is_email_exist(db_session: Session, email: str) -> bool:
        return UserRepository.is_email_exists(db_session, email)

    @staticmethod
    def get_password_hash_by_email(db_session: Session, email: str) -> str | None:
        return UserRepository.get_password_hash_by_email(db_session, email)

    @staticmethod
    def get_user_by_email(db_session: Session, email: str) -> OutUserSchema | None:
        by_email = ByEmail(UserModel.email, email)
        return UserRepository.get_user_by(db_session, by_email)

    @staticmethod
    def get_user_by_uuid(db_session: Session, uuid: UUID) -> OutUserSchema | None:
        by_uuid = ByUUID(UserModel.uuid, uuid)
        return UserRepository.get_user_by(db_session, by_uuid)

    @staticmethod
    def add_user(db_session: Session, schema: InUserSchema) -> OutUserSchema:
        """
        :except UserAlreadyExistsError
        """
        uuid = schema.uuid
        email = schema.email
        if UserService.get_user_by_uuid(db_session, uuid):
            raise UserAlreadyExistsError('uuid', str(uuid))

        if UserService.get_user_by_email(db_session, email):
            raise UserAlreadyExistsError('email', email)

        return UserRepository.add_user(db_session, schema)
