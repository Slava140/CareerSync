import bcrypt
import jwt

from api.v1.auth.schemas.token import AccessTokenPayloadSchema
from config import settings
from errors import InvalidTokenError


def get_hashed_string(string: str) -> str:
    password_bytes = string.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password=password_bytes, salt=salt)
    return hashed_password.decode('utf-8')


def is_correct_hash(plain: str, hashed: str) -> bool:
    password_bytes = plain.encode('utf-8')
    hashed_password_bytes = hashed.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_password_bytes)


def generate_access_token(schema: AccessTokenPayloadSchema) -> str:
    payload = dict(
        sub=str(schema.sub),
        exp=schema.exp
    )
    return jwt.encode(
        payload=payload,
        key=settings.JWT_SECRET,
        algorithm='HS256'
    )


def decode_access_token(token: str) -> AccessTokenPayloadSchema:
    """
    :except InvalidTokenError
    """
    try:
        payload = jwt.decode(
            jwt=token,
            key=settings.JWT_SECRET,
            algorithms=['HS256']
        )
        return AccessTokenPayloadSchema(sub=payload.get('sub'), exp=payload.get('exp'))
    except jwt.InvalidTokenError:
        raise InvalidTokenError
