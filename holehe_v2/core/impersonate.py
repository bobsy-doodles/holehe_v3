"""
Thin async wrapper around curl_cffi — impersonates a real browser TLS fingerprint.
Install: pip install curl-cffi
"""

from typing import Optional
from curl_cffi.requests import AsyncSession


async def impersonate_request_async(
    url: str,
    method: str = "GET",
    headers: Optional[dict] = None,
    data: Optional[dict] = None,
    allow_redirects: bool = True,
    impersonate: str = "chrome120",
):
    async with AsyncSession(impersonate=impersonate) as session:
        return await session.request(
            method,
            url,
            headers=headers or {},
            data=data,
            allow_redirects=allow_redirects,
        )
