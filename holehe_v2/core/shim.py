import sys
from types import ModuleType
from holehe_v2.core.result import Result


def _install() -> None:
    root = ModuleType("user_scanner")
    core = ModuleType("user_scanner.core")
    leaf = ModuleType("user_scanner.core.result")

    leaf.Result = Result

    root.core   = core
    core.result = leaf

    sys.modules.setdefault("user_scanner",             root)
    sys.modules.setdefault("user_scanner.core",        core)
    sys.modules.setdefault("user_scanner.core.result", leaf)


_install()
