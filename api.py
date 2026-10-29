import importfile
import inspect
import os
from typing import List, Optional
import httpx
from holehe_v2.core.base_module import BaseModule
from holehe_v2.core.helpers import get_evasion_client
from holehe_v2.core.result import Result

class EmailScanner:
    """
    Programmatic entry point for embedding holehe_v2 into third-party OSINT pipelines.
    """
    def __init__(self, proxy: Optional[str] = None, concurrency: int = 50):
        self.proxy = proxy
        self.concurrency = concurrency
        self._modules_dir = os.path.join(os.path.dirname(__file__), "modules")

    def _discover_modules(self, client: httpx.AsyncClient) -> List[BaseModule]:
        """Dynamically scans modules/ directory and instantiates valid subclasses."""
        instantiated = []
        for file in os.listdir(self._modules_dir):
            if file.endswith(".py") and not file.startswith("__"):
                module_name = file[:-3]
                file_path = os.path.join(self._modules_dir, file)
                
                # Dynamic file importing
                mod = importfile.importfile(file_path)
                for name, obj in inspect.getmembers(mod, inspect.isclass):
                    if issubclass(obj, BaseModule) and obj is not BaseModule:
                        instantiated.append(obj(client=client))
        return instantiated

    async def scan(self, email: str, target_module: Optional[str] = None) -> List[Result]:
        """
        Scans an target email concurrently across discovered platforms.
        """
        async with get_evasion_client(proxy=self.proxy, concurrency=self.concurrency) as client:
            modules = self._discover_modules(client)
            
            # Filter if running a single, explicit target module check (--module)
            if target_module:
                modules = [m for m in modules if m.name == target_module.lower()]
            
            if not modules:
                return []
                
            # Execute modules concurrently using asyncio.gather
            tasks = [module.check(email) for module in modules]
            import asyncio
            results = await asyncio.gather(*tasks)
            return list(results)
