from holehe_v2.core.base_module import BaseModule
from holehe_v2.core.result import Result
from holehe_v2.core.helpers import apply_jitter

class Office365(BaseModule):
    @property
    def name(self) -> str:
        return "office365"

    async def _check_logic(self, email: str) -> Result:
        # Bypasses basic WAF pattern monitors
        await apply_jitter(50, 200)
        
        url = "https://microsoftonline.com"
        payload = {"username": email, "isOtherUser": True}
        
        # Requests natively borrow parameters directly via proxy and evasion components inherited
        response = await self.client.post(url, json=payload)
        response.raise_for_status()
        data = response.json()
        
        if data.get("IfExistsResult") == 0:
            return Result(platform=self.name, status="[+]", url=url)
        return Result(platform=self.name, status="[-]", url=url)
