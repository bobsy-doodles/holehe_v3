import httpx
from holehe_v2.core.result import Result


async def _check(email: str) -> Result:
    url = "https://www.jeevansathi.com/app-gateway/jsprofilecreator/v1/profile-exists"
    show_url = "https://jeevansathi.com"

    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Mobile Safari/537.36",
        "Accept": "application/json",
        "Accept-Encoding": "identity",
        "Referer": "https://www.jeevansathi.com/",
        "Origin": "https://www.jeevansathi.com",
    }

    try:
        async with httpx.AsyncClient(timeout=15.0, follow_redirects=False) as client:
            response = await client.get(url, headers=headers, params={"email": email})

        if response.status_code == 403:
            return Result.error("Caught by WAF or IP Block (403)")

        if response.status_code == 429:
            return Result.error("Rate limited (429)")

        if response.status_code != 200:
            return Result.error(f"HTTP Error: {response.status_code}")

        data = response.json()
        is_exists = data.get("data", {}).get("isUserExists")

        if is_exists is True:
            return Result.taken(url=show_url)

        if is_exists is False:
            return Result.available(url=show_url)

        return Result.error("Unexpected response body structure, report it via GitHub issues")

    except httpx.ConnectTimeout:
        return Result.error("Connection timed out")

    except httpx.ReadTimeout:
        return Result.error("Server took too long to respond")

    except Exception as e:
        return Result.error(e)


async def validate_jeevansathi(email: str) -> Result:
    return await _check(email)
