import hashlib
from holehe_v2.core.base_module import BaseModule
from holehe_v2.core.result import Result
from holehe_v2.core.helpers import apply_jitter

class Gravatar(BaseModule):
    @property
    def name(self) -> str:
        return "gravatar"

    async def _check_logic(self, email: str) -> Result:
        # Avoid rapid sequential tracking flags
        await apply_jitter(100, 300)
        
        # Gravatar paths rely on a lowercase, stripped MD5 hex string hash signature
        cleaned_email = email.strip().lower()
        email_hash = hashlib.md5(cleaned_email.encode("utf-8")).hexdigest()
        
        url = f"https://gravatar.com{email_hash}.json"
        
        # Dispatch request through the standard client context
        response = await self.client.get(url)
        
        if response.status_code == 200:
            # Successfully found account data
            data = response.json()
            entry = data.get("entry", [{}])[0]
            display_name = entry.get("displayName", "No display name")
            
            return Result(
                platform=self.name, 
                status="[+]", 
                url=url, 
                error=f"Profile: {display_name}"
            )
            
        elif response.status_code == 404:
            # Target identifier not found
            return Result(platform=self.name, status="[-]", url=url)
            
        else:
            # Capture other anomalous status errors elegantly (e.g., 403, 429)
            return Result(
                platform=self.name, 
                status="[!]", 
                url=url, 
                error=f"Unexpected status: {response.status_code}"
            )
