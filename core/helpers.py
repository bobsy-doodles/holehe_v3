import random
import asyncio
import httpx

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0"
]

def get_evasion_client(proxy: str = None, concurrency: int = 50) -> httpx.AsyncClient:
    """
    Constructs an advanced AsyncClient optimized for evasion.
    Enforces HTTP/2, randomized default headers, and robust connection pooling limits.
    """
    limits = httpx.Limits(max_connections=concurrency, max_keepalive_connections=concurrency // 2)
    
    headers = {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "Connection": "keep-alive"
    }
    
    mounts = {}
    if proxy:
        mounts = {"http://": httpx.AsyncProxyTransport(proxy), "https://": httpx.AsyncProxyTransport(proxy)}

    # http2=True matches the network signature of modern browsers, throwing off basic script blockers
    return httpx.AsyncClient(limits=limits, headers=headers, http2=True, mounts=mounts, timeout=10.0)

async def apply_jitter(min_ms: int = 50, max_ms: int = 250):
    """Introduces minor timing anomalies between concurrent worker queries."""
    delay = random.randint(min_ms, max_ms) / 1000.0
    await asyncio.sleep(delay)
