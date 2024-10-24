from fr_common_lib.exc import HTTPException


class ExcAccessTokenExpired(HTTPException):

    message = 'Токен доступа устарел'

    def __init__(self) -> None:
        super().__init__(403)


class ExcRefreshTokenExpired(HTTPException):

    message = 'Токен обновления устарел'

    def __init__(self) -> None:
        super().__init__(401)
