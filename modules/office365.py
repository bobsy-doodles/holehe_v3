from holehe_v2.core.base_module import BaseModule
from holehe_v2.core.result import Result
from holehe_v2.core.helpers import apply_jitter

class Office365(BaseModule):
    @property
    def name(self) -> str:
        return "office365"

    async def _check_logic(self, email: str) -> Result:
        # Bypasses sequential detection heuristics
        await apply_jitter(100, 300) 
        
        url = f"https://microsoftonline.com"
        payload = {"username": email, "isOtherUser": True}
        
        # client configuration inherit headers and proxy properties natively from BaseModule
        response = await self.client.post(url, json=payload)
        data = response.json()
        
        # Example validation structure
        if data.get("IfExistsResult") == 0:
            return Result(platform=self.name, status="[+]", url=url)
        return Result(platform=self.name, status="[-]", url=url)
