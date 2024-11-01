from datetime import datetime

from pydantic import BaseModel, EmailStr, field_validator

from api.v1.profile.schemas.user import OutUserSchema
from api.v1.auth.schemas.refresh_session import OutRefreshSessionSchema
from base_pydantic_types import PasswordStr, MediumStr, ExtraLargeStr, UTCDatetime


class InLoginSchema(BaseModel):
    email:      EmailStr
    password:   PasswordStr


class TokensPairSchema(BaseModel):
    access_token_header_and_payload:    str
    access_token_signature:             str
    access_token_expiration:            UTCDatetime
    refresh_session:                    OutRefreshSessionSchema


class OutLoginSchema(TokensPairSchema):
    user: OutUserSchema
