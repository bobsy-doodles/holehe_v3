from enum import Enum
from typing import Any, Dict, Optional


class Status(Enum):
    TAKEN     = "taken"
    AVAILABLE = "available"
    ERROR     = "error"


class Result:
    def __init__(
        self,
        status: Status,
        url: Optional[str] = None,
        message: Optional[str] = None,
        extra: Optional[Dict[str, Any]] = None,
        media: Optional[Dict[str, Any]] = None,
    ):
        self.status  = status
        self.url     = url
        self.message = message
        self.extra   = extra or {}
        self.media   = media or {}

    @classmethod
    def taken(cls, url=None, extra=None, media=None):
        return cls(Status.TAKEN, url=url, extra=extra, media=media)

    @classmethod
    def available(cls, url=None, extra=None, media=None):
        return cls(Status.AVAILABLE, url=url, extra=extra, media=media)

    @classmethod
    def error(cls, message=None, url=None, extra=None, media=None):
        return cls(Status.ERROR, url=url, message=str(message) if message else "Unknown error", extra=extra, media=media)

    @property
    def is_taken(self) -> bool:
        return self.status == Status.TAKEN

    @property
    def is_available(self) -> bool:
        return self.status == Status.AVAILABLE

    @property
    def is_error(self) -> bool:
        return self.status == Status.ERROR

    def __repr__(self) -> str:
        return f"Result(status={self.status.value}, url={self.url!r}, message={self.message!r}, extra={self.extra!r})"
