from datetime import datetime, timezone
from uuid import UUID

from pydantic import BaseModel, Field

from api.v1.auth.utils import get_access_token_exp
from base_pydantic_types import UTCDatetime


class AccessTokenSchema(BaseModel):
    sub: UUID
    exp: UTCDatetime = Field(default_factory=get_access_token_exp)


class FingerprintSchema(BaseModel):
    user_ip:            str
    user_agent:         str
    accept_language:    str
