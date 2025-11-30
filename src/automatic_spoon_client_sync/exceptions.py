from dataclasses import dataclass

from pytsterrors import TSTError


@dataclass
class ErrorField:
    field: str
    error: str


class CreationError(TSTError):
    def __init__(
        self,
        tag: str,
        message: str,
        error_fields: list[ErrorField],
    ):
        super().__init__(tag, message)
        self.error_fields = error_fields
