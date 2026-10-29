import abc
import httpx
from holehe_v2.core.result import Result

class BaseModule(abc.ABC):
    """
    Abstract Base Class that every custom website scanner must inherit from.
    """
    def __init__(self, client: httpx.AsyncClient):
        self.client = client

    @property
    @abc.abstractmethod
    def name(self) -> str:
        """The lowercase string identifying the module platform name."""
        pass

    @abc.abstractmethod
    async def _check_logic(self, email: str) -> Result:
        """Core API probing logic belonging to specific site integrations."""
        pass

    async def check(self, email: str) -> Result:
        """Safely wrapper engine processing errors elegantly to protect scanner workflow loops."""
        try:
            return await self._check_logic(email)
        except httpx.TimeoutException:
            return Result(platform=self.name, status="[!]", url="", error="Timeout")
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 429:
                return Result(platform=self.name, status="[!]", url="", error="Rate Limited (429)")
            return Result(platform=self.name, status="[!]", url="", error=f"HTTP Status {e.response.status_code}")
        except Exception as e:
            return Result(platform=self.name, status="[!]", url="", error=str(e))
