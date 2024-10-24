from attrs import define
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from typing import Type, TypeVar

from pydantic import BaseModel

from .exc import ExcInvalidUrlToken, ExcUrlTokenExpired
from .schemas import UrlTokenPayload

T = TypeVar("T", bound=BaseModel)

@define
class UrlTokenSvc:

    _url_serializer:URLSafeTimedSerializer

    def encode(self, payload: T) -> str:
        payload = UrlTokenPayload(action=payload.__class__.__name__, payload=payload)
        return self._url_serializer.dumps(payload.model_dump())

    def decode(self, token: str, payload_type: Type[T], ttl: int = 1200) -> UrlTokenPayload[T]:

        try:
            decoded = self._url_serializer.loads(token, max_age=ttl)
            token_payload = UrlTokenPayload[payload_type].model_validate(decoded)
        except SignatureExpired:
            raise ExcUrlTokenExpired()
        except Exception:
            raise ExcInvalidUrlToken()

        if token_payload.action != payload_type.__name__:
            raise ExcInvalidUrlToken()

        return token_payload
