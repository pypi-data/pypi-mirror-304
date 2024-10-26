from fr_common_lib.utils.json_example import JsonExample


class HTTPException(Exception):

    message: str = None
    type: str = None

    def __init__(
        self,
        status_code: int,
        message: str = None,
        headers: dict[str, str] | None = None,
        **detail
    ) -> None:
        self.status_code = status_code
        self.payload = detail | {'message': message or self.message, 'type': self.__class__.__name__}
        self.headers = headers

    def __str__(self) -> str:
        return f"{self.status_code}: {self.payload}"

    def __repr__(self) -> str:
        class_name = self.__class__.__name__
        return f"{class_name}(status_code={self.status_code!r}, detail={self.payload!r})"

    @classmethod
    def example(cls) -> JsonExample:
        return JsonExample(cls)

