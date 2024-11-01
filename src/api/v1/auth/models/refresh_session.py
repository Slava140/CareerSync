from sqlalchemy.orm import Mapped

from database import Base, pk_uuid_v7, fk_user_uuid, str_90_unique, str_300, datetime_utc_tz


class RefreshSessionModel(Base):
    __tablename__ = 'refresh_sessions'

    uuid:           Mapped[pk_uuid_v7]
    user_uuid:      Mapped[fk_user_uuid]
    refresh_token:  Mapped[str_90_unique]
    expires_in:     Mapped[datetime_utc_tz]
