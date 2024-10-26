import datetime as dt
import uuid

from pydantic import BaseModel
from pydantic import Field


class JwtPayload(BaseModel):

    iss: str = Field(default='facereg', description='issuer издатель')
    jti: str = Field(description='jwt token identifier', default_factory=lambda: str(uuid.uuid4()))
    iat: int = Field(
        default_factory=lambda: int(dt.datetime.now(tz=dt.timezone.utc).timestamp()),
        description='issued at момент издания unix time'
    )
    exp: int = Field(description='expired действует до unix time')
    sub: str = Field(description='subject идентификатор пользователя')
    typ: str = Field(description='тип токена', default='jwt')

    knd: str = Field(description='вид токена refresh или access')
    sid: str = Field(description='идентификатор сессии')
    cid: int = Field(description='идентификатор клиента')

    @property
    def exp_dt(self) -> dt.datetime:
        return dt.datetime.fromtimestamp(self.exp, tz=dt.timezone.utc)

    @property
    def iat_dt(self) -> dt.datetime:
        return dt.datetime.fromtimestamp(self.iat, tz=dt.timezone.utc)


class JwtToken(BaseModel):
    encoded: str
    payload: JwtPayload

class AccessToken(JwtToken):

    @classmethod
    def cookie_key(cls) -> str:
        return 'X-Access-Token'

class RefreshToken(JwtToken):

    @classmethod
    def cookie_key(cls) -> str:
        return 'X-Refresh-Token'

class JwtPair(BaseModel):
    access_token: AccessToken
    refresh_token: RefreshToken


