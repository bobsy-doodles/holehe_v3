class Result:
    """
    Standard data object returned by all module scanners.
    """
    def __init__(self, platform: str, status: str, url: str, error: str = ""):
        self.platform = platform
        self.status = status  # [+], [-], or [!]
        self.url = url
        self.error = error

    def to_dict(self) -> dict:
        return {
            "platform": self.platform,
            "status": self.status,
            "url": self.url,
            "error": self.error
        }

    def __str__(self) -> str:
        err_msg = f" ({self.error})" if self.error else ""
        return f"{self.status} {self.platform}{err_msg}"
