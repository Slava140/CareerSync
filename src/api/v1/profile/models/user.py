from sqlalchemy.orm import Mapped

from api.v1.profile.models.enums import Role
from database import (
    Base, pk_uuid_v7,
    str_90, str_30_unique,
    created_at, updated_at, str_60, str_60_unique
)


class UserModel(Base):
    __tablename__ = 'users'

    uuid:               Mapped[pk_uuid_v7]
    first_name:         Mapped[str_60]
    middle_name:        Mapped[str_60]
    last_name:          Mapped[str_60]
    email:              Mapped[str_60_unique | None]
    hashed_password:    Mapped[str_90]
    phone_number:       Mapped[str_30_unique | None]
    role:               Mapped[Role | None]
    created_at:         Mapped[created_at]
    updated_at:         Mapped[updated_at]
