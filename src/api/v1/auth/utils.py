from datetime import datetime, timezone

import bcrypt
import jwt

from api.v1.auth.schemas.token import AccessTokenSchema
from config import settings
from errors import InvalidTokenError


def get_access_token_exp():
    return datetime.now(tz=timezone.utc) + settings.access_token_ttl_timedelta


def get_refresh_token_exp():
    return datetime.now(tz=timezone.utc) + settings.refresh_token_ttl_timedelta


def get_hashed_string(string: str) -> str:
    password_bytes = string.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password=password_bytes, salt=salt)
    return hashed_password.decode('utf-8')


def is_correct_hash(plain: str, hashed: str) -> bool:
    password_bytes = plain.encode('utf-8')
    hashed_password_bytes = hashed.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_password_bytes)


def generate_access_token(schema: AccessTokenSchema) -> str:
    payload = dict(
        sub=str(schema.sub),
        exp=schema.exp
    )
    return jwt.encode(
        payload=payload,
        key=settings.JWT_SECRET,
        algorithm='HS256'
    )


def decode_access_token(token: str) -> AccessTokenSchema:
    """
    :except InvalidTokenError
    """
    try:
        payload = jwt.decode(
            jwt=token,
            key=settings.JWT_SECRET,
            algorithms=['HS256']
        )
        return AccessTokenSchema(sub=payload.get('sub'), exp=payload.get('exp'))
    except jwt.InvalidTokenError:
        raise InvalidTokenError
