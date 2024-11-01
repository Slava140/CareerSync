import re
from datetime import datetime, timezone
from typing import Annotated
from uuid import UUID

from uuid_extensions import uuid7
from pydantic import Field, BaseModel, BeforeValidator, EmailStr, AfterValidator


def password_validator(value: str) -> str:
    if len(value) < 8:
        raise ValueError('Password length must be greater or equal than 8')

    if len(value) > 20:
        raise ValueError('Password length must be less or equal than 20')

    if not re.search(r'\d', value):
        raise ValueError('Password must contain at least one digit')

    # Проверка на наличие заглавных букв
    if not re.search(r'[A-Z]', value):
        raise ValueError('Password must contain at least one uppercase letter')

    # Проверка на наличие строчных букв
    if not re.search(r'[a-z]', value):
        raise ValueError('Password must contain at least one lowercase letter')

    return value


def is_utc_datetime_validator(value: datetime) -> datetime:
    tz = value.tzinfo
    if tz is timezone.utc:
        return value
    else:
        raise ValueError('datetime must have a UTC timezone.')


UUID7 = Annotated[UUID, Field(default_factory=uuid7)]
PasswordStr = Annotated[str, BeforeValidator(password_validator)]
UTCDatetime = Annotated[datetime, AfterValidator(is_utc_datetime_validator)]

TinyStr = Annotated[str, Field(max_length=30)]
SmallStr = Annotated[str, Field(max_length=60)]
MediumStr = Annotated[str, Field(max_length=90)]
LargeStr = Annotated[str, Field(max_length=150)]
ExtraLargeStr = Annotated[str, Field(max_length=300)]

