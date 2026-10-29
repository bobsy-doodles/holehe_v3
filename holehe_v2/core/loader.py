import importlib.util
import inspect
import os
from pathlib import Path
from typing import Callable, Dict

import holehe_v2.core.shim  # noqa: F401 — must run before any module import


def _modules_dir() -> Path:
    return Path(__file__).parent.parent / "modules"


def load_validators(modules_path: Path | None = None) -> Dict[str, Callable]:
    directory = modules_path or _modules_dir()
    validators: Dict[str, Callable] = {}

    for filepath in sorted(directory.glob("*.py")):
        if filepath.name.startswith("_"):
            continue

        module_name = f"holehe_v2.modules.{filepath.stem}"
        spec   = importlib.util.spec_from_file_location(module_name, filepath)
        module = importlib.util.module_from_spec(spec)

        try:
            spec.loader.exec_module(module)
        except Exception as e:
            print(f"[loader] Failed to load {filepath.name}: {e}")
            continue

        for name, fn in inspect.getmembers(module, inspect.iscoroutinefunction):
            if name.startswith("validate_"):
                platform = name[len("validate_"):]
                validators[platform] = fn

    return validators
