import httpx
from holehe_v2.core.result import Result


async def _check(email: str) -> Result:
    url = f"https://www.naukri.com/cloudgateway-mynaukri/resman-aggregator-services/v0/accounts/{email}"
    show_url = "https://naukri.com"

    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Mobile Safari/537.36",
        "Accept": "*/*",
        "Referer": "https://www.naukri.com/registration/createAccount?othersrcp=19102",
        "appid": "135",
        "systemid": "135",
        "clientid": "m0b5",
    }

    try:
        async with httpx.AsyncClient(timeout=15.0, follow_redirects=False) as client:
            response = await client.head(url, headers=headers)

        if response.status_code == 403:
            return Result.error("Caught by WAF or IP Block (403)")

        if response.status_code == 429:
            return Result.error("Rate limited (429)")

        if response.status_code == 200:
            return Result.taken(url=show_url)

        if response.status_code == 404:
            return Result.available(url=show_url)

        return Result.error(f"HTTP Error: {response.status_code}")

    except httpx.ConnectTimeout:
        return Result.error("Connection timed out")

    except httpx.ReadTimeout:
        return Result.error("Server took too long to respond")

    except Exception as e:
        return Result.error(e)


async def validate_naukri(email: str) -> Result:
    return await _check(email)
