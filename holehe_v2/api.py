import os
import importlib.util
import inspect
from typing import List, Optional
from holehe_v2.core.base_module import BaseModule
from holehe_v2.core.helpers import get_evasion_client
from holehe_v2.core.result import Result

class EmailScanner:
    """
    The main SDK / Library engine class for running scans programmatically.
    """
    def __init__(self, proxy: Optional[str] = None, concurrency: int = 50):
        self.proxy = proxy
        self.concurrency = concurrency
        self._modules_dir = os.path.join(os.path.dirname(__file__), "modules")

    def _discover_modules(self) -> List[type]:
        """Dynamically inspects files inside modules directory to pick up class configurations."""
        classes = []
        if not os.path.isdir(self._modules_dir):
            return classes

        for file in os.listdir(self._modules_dir):
            if file.endswith(".py") and not file.startswith("__"):
                module_name = file[:-3]
                file_path = os.path.join(self._modules_dir, file)
                
                # Dynamic compilation context setup
                spec = importlib.util.spec_from_file_location(module_name, file_path)
                if spec and spec.loader:
                    mod = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(mod)
                    
                    for _, obj in inspect.getmembers(mod, inspect.isclass):
                        if issubclass(obj, BaseModule) and obj is not BaseModule:
                            classes.append(obj)
        return classes

    async def scan(self, email: str, only_module: Optional[str] = None) -> List[Result]:
        """Runs the email target concurrently across active discovered platform classes."""
        async with get_evasion_client(proxy=self.proxy, concurrency=self.concurrency) as client:
            module_classes = self._discover_modules()
            
            # Instantiating the discovered class types with client injection
            modules = [cls(client) for cls in module_classes]
            
            if only_module:
                modules = [m for m in modules if m.name == only_module.lower()]

            if not modules:
                return []

            import asyncio
            tasks = [module.check(email) for module in modules]
            return list(await asyncio.gather(*tasks))
