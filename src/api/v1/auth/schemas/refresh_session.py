from datetime import datetime, timezone
from uuid import UUID

from pydantic import BaseModel, Field

from api.v1.auth.utils import get_refresh_token_exp
from base_pydantic_types import UUID7, UTCDatetime
from config import settings


class RefreshSessionSchema(BaseModel):
    uuid:           UUID7
    user_uuid:      UUID
    refresh_token:  str
    expires_in:     UTCDatetime = Field(default_factory=get_refresh_token_exp)
