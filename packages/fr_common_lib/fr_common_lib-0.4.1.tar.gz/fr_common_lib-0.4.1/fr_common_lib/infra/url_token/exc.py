from fr_common_lib.exc import HTTPException


class ExcInvalidUrlToken(HTTPException):

    message = 'Неверный url токен'

    def __init__(self) -> None:
        super().__init__(400)


class ExcUrlTokenExpired(HTTPException):

    message = 'Токен устарел'

    def __init__(self) -> None:
        super().__init__(400)
