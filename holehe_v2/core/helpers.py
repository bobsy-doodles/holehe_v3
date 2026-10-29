import random
import asyncio
import httpx

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0"
]

def get_evasion_client(proxy: str = None, concurrency: int = 50) -> httpx.AsyncClient:
    """Configures a high-performance HTTP/2 browser proxy engine built to drop anti-bot flags."""
    limits = httpx.Limits(max_connections=concurrency, max_keepalive_connections=concurrency // 2)
    
    headers = {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "keep-alive"
    }
    
    mounts = {}
    if proxy:
        mounts = {"http://": httpx.AsyncProxyTransport(proxy), "https://": httpx.AsyncProxyTransport(proxy)}

    return httpx.AsyncClient(limits=limits, headers=headers, http2=True, mounts=mounts, timeout=10.0)

async def apply_jitter(min_ms: int = 50, max_ms: int = 250):
    """Adds artificial microscopic timing discrepancies between worker task dispatches."""
    await asyncio.sleep(random.randint(min_ms, max_ms) / 1000.0)
