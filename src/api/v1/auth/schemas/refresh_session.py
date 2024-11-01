from datetime import datetime, timezone
from uuid import UUID

from pydantic import BaseModel, Field
from base_pydantic_types import UUID7, UTCDatetime
from config import settings


def get_refresh_token_exp():
    return datetime.now(tz=timezone.utc) + settings.refresh_token_ttl_timedelta


class BaseRefreshSessionSchema(BaseModel):
    uuid:           UUID7
    user_uuid:      UUID
    refresh_token:  str
    expires_in:     UTCDatetime = Field(default_factory=get_refresh_token_exp)


class InRefreshSessionSchema(BaseRefreshSessionSchema):
    ...


class OutRefreshSessionSchema(BaseRefreshSessionSchema):
    ...
