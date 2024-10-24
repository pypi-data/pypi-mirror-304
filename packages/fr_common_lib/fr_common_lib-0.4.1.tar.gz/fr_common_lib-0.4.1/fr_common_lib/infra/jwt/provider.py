from dishka import Provider, provide, Scope
from .config import JwtConfig
from .service import JwtSvc

class JwtProv(Provider):

    @provide(scope=Scope.APP)
    def config(self) -> JwtConfig:
        return JwtConfig()

    service = provide(JwtSvc, scope=Scope.APP)

