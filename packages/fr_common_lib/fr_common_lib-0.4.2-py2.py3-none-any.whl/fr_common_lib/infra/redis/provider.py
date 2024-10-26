from dishka import Provider, provide, Scope
from redis.client import Redis

from . import RedisConfig


class RedisProv(Provider):

    @provide(scope=Scope.APP)
    def config(self) -> RedisConfig:
        return RedisConfig()

    @provide(scope=Scope.APP)
    def client(self, config: RedisConfig) -> Redis:
        return Redis(
            config.URL,
            encoding="utf-8",
            decode_responses=True
        )


