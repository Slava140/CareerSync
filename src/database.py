from datetime import datetime
from typing import Annotated
from uuid import UUID

from sqlalchemy import String, text, ForeignKey, DateTime
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import DeclarativeBase, registry, mapped_column, sessionmaker

from config import settings

engine = create_engine(url=settings.database_url_psycopg, echo=False, connect_args={"options": "-c timezone=utc"})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


sql_utc_now = text("timezone('utc', now())")

str_300 = Annotated[str, 300]
str_150 = Annotated[str, 150]
str_90 = Annotated[str, 90]
str_60 = Annotated[str, 60]
str_30 = Annotated[str, 30]

str_30_unique = Annotated[str, mapped_column(String(30), unique=True)]
str_60_unique = Annotated[str, mapped_column(String(60), unique=True)]
str_90_unique = Annotated[str, mapped_column(String(90), unique=True)]

pk_int = Annotated[int, mapped_column(primary_key=True)]
pk_uuid_v7 = Annotated[UUID, mapped_column(primary_key=True)]
fk_user_uuid = Annotated[UUID, mapped_column(ForeignKey(column='users.uuid', ondelete='CASCADE'))]

created_at = Annotated[datetime, mapped_column(DateTime(timezone=True), server_default=sql_utc_now)]
updated_at = Annotated[datetime, mapped_column(DateTime(timezone=True), server_default=sql_utc_now, onupdate=sql_utc_now)]

datetime_utc_tz = Annotated[datetime, mapped_column(DateTime(timezone=True))]


class Base(DeclarativeBase):
    registry = registry(
        type_annotation_map={
            str_300: String(300),
            str_150: String(150),
            str_90: String(90),
            str_60: String(60),
            str_30: String(30),
        }
    )
