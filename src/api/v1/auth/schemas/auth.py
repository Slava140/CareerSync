from datetime import datetime, timezone
from uuid import UUID

from pydantic import BaseModel, EmailStr, field_validator, Field

from api.v1.profile.schemas.user import OutUserSchema
# from api.v1.auth.schemas.refresh_session import RefreshSessionSchema
from base_pydantic_types import PasswordStr, MediumStr, ExtraLargeStr, UTCDatetime, UUID7
from config import settings


def get_access_token_exp():
    return datetime.now(tz=timezone.utc) + settings.access_token_ttl_timedelta


def get_refresh_token_exp():
    return datetime.now(tz=timezone.utc) + settings.refresh_token_ttl_timedelta


class AccessTokenSchema(BaseModel):
    sub: UUID
    exp: UTCDatetime = Field(default_factory=get_access_token_exp)


class FingerprintSchema(BaseModel):
    user_ip:            str
    user_agent:         str
    accept_language:    str


class RefreshSessionSchema(BaseModel):
    uuid:           UUID7
    user_uuid:      UUID
    refresh_token:  str
    expires_in:     UTCDatetime = Field(default_factory=get_refresh_token_exp)


class TokensPairSchema(BaseModel):
    access_token_header_and_payload:    str
    access_token_signature:             str
    access_token_expiration:            UTCDatetime
    refresh_session:                    RefreshSessionSchema


class InLoginSchema(BaseModel):
    email:      EmailStr
    password:   PasswordStr


class OutLoginSchema(TokensPairSchema):
    user: OutUserSchema
