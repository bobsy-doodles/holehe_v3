import httpx
import abc
from holehe_v2.core.result import Result

class BaseModule(abc.ABC):
    """
    Abstract Base Class that every holehe_v2 module must inherit from.
    """
    def __init__(self, client: httpx.AsyncClient):
        self.client = client

    @property
    @abc.abstractmethod
    def name(self) -> str:
        """Return the clean lowercase name of the platform."""
        pass

    @abc.abstractmethod
    async def _check_logic(self, email: str) -> Result:
        """Internal method containing the specific API logic for the platform."""
        pass

    async def check(self, email: str) -> Result:
        """
        Wrapper method executed by the core runner. 
        Safely catches network exceptions, timeouts, and unexpected errors.
        """
        try:
            return await self._check_logic(email)
        except httpx.TimeoutException:
            return Result(platform=self.name, status="[!]", url="", error="Timeout reached")
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 429:
                return Result(platform=self.name, status="[!]", url="", error="Rate limited (429)")
            return Result(platform=self.name, status="[!]", url="", error=f"HTTP Error {e.response.status_code}")
        except Exception as e:
            return Result(platform=self.name, status="[!]", url="", error=str(e))
