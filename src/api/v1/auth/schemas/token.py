from datetime import datetime, timezone
from uuid import UUID

from pydantic import BaseModel, Field

from base_pydantic_types import UTCDatetime
from config import settings


def get_access_token_exp():
    return datetime.now(tz=timezone.utc) + settings.access_token_ttl_timedelta


class BaseAccessTokenSchema(BaseModel):
    sub: UUID
    exp: UTCDatetime = Field(default_factory=get_access_token_exp)


class AccessTokenPayloadSchema(BaseAccessTokenSchema):
    ...


class FingerprintSchema(BaseModel):
    user_ip:            str
    user_agent:         str
    accept_language:    str
