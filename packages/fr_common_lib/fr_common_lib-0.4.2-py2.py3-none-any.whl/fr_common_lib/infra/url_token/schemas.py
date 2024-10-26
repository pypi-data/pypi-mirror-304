
from typing import Generic, TypeVar
from pydantic import BaseModel


T = TypeVar('T', bound=BaseModel)
class UrlTokenPayload(BaseModel,Generic[T]):
    action: str
    payload: T


