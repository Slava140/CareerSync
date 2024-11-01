from abc import ABC, abstractmethod
from typing import Any, Protocol
from uuid import UUID

from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import InstrumentedAttribute

from api.v1.profile.models.user import UserModel


class ByObject(ABC):
    @property
    @abstractmethod
    def key(self) -> InstrumentedAttribute:
        ...

    @property
    @abstractmethod
    def value(self) -> str:
        ...


class ByEmail(ByObject):
    def __init__(self, by: InstrumentedAttribute, email: str):
        self._by = by
        self._email = email

    @property
    def key(self) -> InstrumentedAttribute:
        return self._by

    @property
    def value(self) -> str:
        return self._email


class ByUUID(ByObject):
    def __init__(self, by: InstrumentedAttribute, uuid: UUID):
        self._by = by
        self._uuid = uuid

    @property
    def key(self) -> InstrumentedAttribute:
        return self._by

    @property
    def value(self) -> str:
        return str(self._uuid)


class ByToken(ByObject):
    def __init__(self, by: InstrumentedAttribute, token: str):
        self._by = by
        self._token = token

    @property
    def key(self) -> InstrumentedAttribute:
        return self._by

    @property
    def value(self) -> str:
        return str(self._token)
