from typing import Generic, TypeVar, Union

T = TypeVar('T')

class Result(Generic[T]):

    def __init__(self, value: Union[T, Exception]):
        if isinstance(value, Exception):
            self._value = None
            self._error = value
        else:
            self._value = value
            self._error = None

    @property
    def value(self) -> T:
        if self.is_err:
            raise ValueError("Cannot access value of an error result")
        return self._value

    @property
    def err(self) -> Exception:
        if not self.is_err:
            raise ValueError("Cannot access error of a value result")
        return self._error

    @property
    def is_err(self) -> bool:
        return self._error is not None