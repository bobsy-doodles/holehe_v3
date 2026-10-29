import asyncio
import inspect
from typing import Callable, Dict, Optional

from holehe_v2.core.result import Result


async def run_all(
    email: str,
    validators: Dict[str, Callable],
    results: Dict[str, Result],
    concurrency: int = 50,
    proxy: Optional[str] = None,
) -> None:
    semaphore = asyncio.Semaphore(concurrency)

    async def _guarded(platform: str, fn: Callable) -> None:
        async with semaphore:
            try:
                sig = inspect.signature(fn)
                if "proxy" in sig.parameters:
                    results[platform] = await fn(email, proxy=proxy)
                else:
                    results[platform] = await fn(email)
            except Exception as e:
                results[platform] = Result.error(str(e))

    await asyncio.gather(*[
        _guarded(platform, fn)
        for platform, fn in validators.items()
    ])
