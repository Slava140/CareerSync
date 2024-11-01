import re
from datetime import datetime

from pydantic import BaseModel, EmailStr, field_validator
from pydantic_extra_types.phone_numbers import PhoneNumber

from base_pydantic_types import UUID7, SmallStr, PasswordStr, UTCDatetime
from api.v1.profile.models.enums import Role


class BaseUserSchema(BaseModel):
    uuid: UUID7
    first_name: SmallStr
    middle_name: SmallStr
    last_name: SmallStr
    email: EmailStr | None = None
    phone_number: PhoneNumber | None = None
    role: Role | None = None


class InUserSchema(BaseUserSchema):
    password: PasswordStr


class OutUserSchema(BaseUserSchema):
    created_at: UTCDatetime
    updated_at: UTCDatetime
