import datetime as dt
import uuid
from typing import Type

import jwt
from attr import define

from .config import JwtConfig
from .exc import ExcAccessTokenExpired, ExcRefreshTokenExpired
from .schemas import JwtPair, JwtToken, JwtPayload, AccessToken, RefreshToken
from ...exc import HTTPException


@define
class JwtSvc:

    _settings: JwtConfig

    def token_pair(
            self,
            sub: str,
            cid: int
    ) -> JwtPair:

        sid = str(uuid.uuid4())

        return JwtPair(
            access_token=self.token(sub=sub, cid=cid, sid=sid, cls=AccessToken),
            refresh_token=self.token(sub=sub, cid=cid, sid=sid, cls=RefreshToken),
        )

    def refresh_pair(
            self,
            refresh_token: JwtToken,
    ) -> JwtPair:
        payload = refresh_token.payload
        return JwtPair(
            access_token=self.token(sub=payload.sub, cid=payload.cid, sid=payload.sid, cls=AccessToken),
            refresh_token=self.token(sub=payload.sub, cid=payload.cid, sid=payload.sid, cls=RefreshToken),
        )


    def token(
            self,
            sub: str, cid: int,
            sid: str, cls: Type[JwtToken],
    ) -> JwtToken:

        exp_td = dt.timedelta(
            minutes=self._settings.ACCESS_EXP if cls == AccessToken else self._settings.REFRESH_EXP
        )
        now = dt.datetime.now(tz=dt.timezone.utc)
        exp = int((now + exp_td).timestamp())

        payload = JwtPayload(knd=cls.__name__, sub=sub, cid=cid, sid=sid, exp=exp)

        encoded = jwt.encode(
            payload=payload.model_dump(),
            key=self._settings.SECRET_KEY,
            algorithm=self._settings.ALG,
        )

        return cls(
            encoded=encoded,
            payload=payload,
        )

    def decode(self, token: str, **options) -> JwtToken:

        def token_payload(encoded, params) -> JwtPayload:
            return JwtPayload(**jwt.decode(
                encoded,
                key=self._settings.SECRET_KEY,
                algorithms=[self._settings.ALG],
                options=params,
            ))

        payload = None
        try:
            payload = token_payload(token, options)
        except jwt.ExpiredSignatureError as exc:
            payload = token_payload(token, options | {'verify_exp': False})
            if payload.knd == AccessToken.__name__:
                raise ExcAccessTokenExpired()
            elif payload.knd == RefreshToken.__name__:
                raise ExcRefreshTokenExpired()
            else:
                raise ValueError(payload.knd)
        except jwt.InvalidTokenError as exc:
            raise HTTPException(400, str(exc))

        cls = globals()[payload.knd]

        return cls(payload=payload, encoded=token)
