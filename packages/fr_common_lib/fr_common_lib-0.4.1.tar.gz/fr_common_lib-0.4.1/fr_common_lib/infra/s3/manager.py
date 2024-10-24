import asyncio
from types_aiobotocore_s3.client import S3Client
from types_aiobotocore_s3.type_defs import PutObjectOutputTypeDef
from typing import TypedDict, NotRequired, Iterable


class S3ObjDescr(TypedDict):
    bucket: NotRequired[str]
    key: str
    body: bytes


class S3Manager:

    def __init__(
        self,
        client: S3Client,
        default_bucket: str | None = None
    ):
        self.default_bucket: str = default_bucket
        self._client = client

        print('Я s3 менеджер синглтон появляюсь')

    async def _put_object(self, obj: S3ObjDescr) ->  PutObjectOutputTypeDef:
        resp = await self._client.put_object(
            Bucket=obj.get('bucket') or self.default_bucket,
            Key=obj['key'], Body=obj['body']
        )
        return resp

    async def put_objects(self, objects: Iterable[S3ObjDescr]) -> list[PutObjectOutputTypeDef]:
        async with asyncio.TaskGroup() as tg:
            tasks = [tg.create_task(self._put_object(obj)) for obj in objects]
        return [task.result() for task in tasks]




