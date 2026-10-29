import sys
import time
import asyncio
import shutil
from typing import Dict, Callable, Optional
from holehe_v2.core.result import Result, Status

# ── Colours ────────────────────────────────────────────────────────────────
RESET   = "\033[0m"
BOLD    = "\033[1m"
DIM     = "\033[2m"

WHITE   = "\033[97m"
RED     = "\033[91m"
GREEN   = "\033[92m"
YELLOW  = "\033[93m"
BLUE    = "\033[94m"
MAGENTA = "\033[95m"
CYAN    = "\033[96m"

USE_COLOUR = True


def _c(code: str) -> str:
    return code if USE_COLOUR else ""


def disable_colour() -> None:
    global USE_COLOUR
    USE_COLOUR = False


# ── Banner ─────────────────────────────────────────────────────────────────
BANNER_LINE1 = "█░█ █▀█ █░░ █▀▀ █░█ █▀▀   █░█ ▀█"
BANNER_LINE2 = "█▀█ █▄█ █▄▄ ██▄ █▀█ ██▄   ▀▄▀ █▄"
SUBTITLE     = "Modern Day Email Intelligence & Reconnaissance Suite"
DEV          = "Developer: Anubhav Kashyap  |  GitHub/Telegram: anubhavanonymous"


def _pad(text: str) -> str:
    cols = shutil.get_terminal_size(fallback=(80, 24)).columns
    pad  = max(0, (cols - len(text)) // 2)
    return " " * pad


def print_banner() -> None:
    print()
    print(f"{_pad(BANNER_LINE1)}{_c(WHITE)}{_c(BOLD)}{BANNER_LINE1}{_c(RESET)}")
    print(f"{_pad(BANNER_LINE2)}{_c(RED)}{_c(BOLD)}{BANNER_LINE2}{_c(RESET)}")
    print()
    print(f"{_pad(SUBTITLE)}{_c(RED)}{SUBTITLE}{_c(RESET)}")
    print(f"{_pad(DEV)}{_c(DIM)}{DEV}{_c(RESET)}")
    print()

# ── Progress bar ───────────────────────────────────────────────────────────
async def progress_bar(
    validators: Dict[str, Callable],
    results: Dict[str, Result],
    total: int,
    width: int = 40,
) -> None:
    cols    = shutil.get_terminal_size(fallback=(80, 24)).columns
    bar_vis = width + 2 + 5 + 2 + len(str(total)) * 2 + 1 + 6
    indent  = " " * max(0, (cols - bar_vis) // 2)

    start = time.monotonic()
    while True:
        done    = len(results)
        frac    = done / total if total else 1
        filled  = int(width * frac)
        bar     = f"{_c(GREEN)}{'█' * filled}{_c(DIM)}{'░' * (width - filled)}{_c(RESET)}"
        pct     = int(frac * 100)
        elapsed = time.monotonic() - start

        sys.stdout.write(
            f"\r{indent}{_c(CYAN)}[{bar}{_c(CYAN)}]{_c(RESET)} "
            f"{_c(BOLD)}{pct:>3}%{_c(RESET)}  "
            f"{_c(GREEN)}{done}{_c(RESET)}/{_c(BOLD)}{total}{_c(RESET)}  "
            f"{_c(DIM)}{elapsed:.1f}s{_c(RESET)}  "
        )
        sys.stdout.flush()

        if done >= total:
            break
        await asyncio.sleep(0.1)

    sys.stdout.write("\n")
    sys.stdout.flush()

# ── Category colours ───────────────────────────────────────────────────────
CATEGORY_COLOURS = {
    "Dev":           BLUE,
    "Shopping":      MAGENTA,
    "Music":         CYAN,
    "Learning":      YELLOW,
    "Social":        GREEN,
    "Jobs":          WHITE,
    "Hosting":       CYAN,
    "Pipeline":      BLUE,
    "Entertainment": MAGENTA,
}


def _cat_colour(category: str) -> str:
    return CATEGORY_COLOURS.get(category, DIM)


# ── Print results ──────────────────────────────────────────────────────────
def print_results(
    email: str,
    results: Dict[str, Result],
    elapsed: float,
    show_errors: bool = False,
    only_used: bool   = False,
) -> None:
    taken     = {p: r for p, r in results.items() if r.is_taken}
    available = {p: r for p, r in results.items() if r.is_available}
    errors    = {p: r for p, r in results.items() if r.is_error}

    # Base indent — centred on the widest expected line
    cols     = shutil.get_terminal_size(fallback=(80, 24)).columns
    content  = 55  # approx width of content block
    indent   = " " * max(0, (cols - content) // 2)

    sep = f"{indent}{_c(DIM)}{'─' * 55}{_c(RESET)}"

    print()
    print(f"{indent}{_c(BOLD)}Target :{_c(RESET)} {_c(CYAN)}{email}{_c(RESET)}")
    print(
        f"{indent}{_c(BOLD)}Modules:{_c(RESET)} {len(results)}  "
        f"{_c(GREEN)}[+] Found: {len(taken)}{_c(RESET)}  "
        f"{_c(DIM)}[-] Not found: {len(available)}{_c(RESET)}  "
        f"{_c(YELLOW)}[!] Errors: {len(errors)}{_c(RESET)}"
    )
    print(sep)
    print()

    # ── Taken
    for platform, result in sorted(taken.items()):
        category = (result.extra or {}).get("category", "")
        cat_str  = f"  {_c(_cat_colour(category))}{_c(BOLD)}({category}){_c(RESET)}" if category else ""
        url_str  = f"  {_c(DIM)}{result.url}{_c(RESET)}" if result.url else ""
        print(f"{indent}{_c(GREEN)}[+]{_c(RESET)} {_c(BOLD)}{platform:<22}{_c(RESET)}{cat_str}{url_str}")

        if result.extra:
            for k, v in result.extra.items():
                if k == "category" or v is None:
                    continue
                print(f"{indent}     {_c(DIM)}└─{_c(RESET)} {_c(CYAN)}{k.capitalize()}: {_c(BOLD)}{v}{_c(RESET)}")

    # ── Available
    if not only_used:
        print()
        for platform, result in sorted(available.items()):
            category = (result.extra or {}).get("category", "")
            cat_str  = f"  {_c(DIM)}({category}){_c(RESET)}" if category else ""
            print(f"{indent}{_c(DIM)}[-] {platform:<22}{_c(RESET)}{cat_str}")

    # ── Errors
    if errors:
        print()
        for platform, result in sorted(errors.items()):
            msg = f"  {_c(DIM)}{result.message}{_c(RESET)}" if show_errors else ""
            print(f"{indent}{_c(YELLOW)}[!]{_c(RESET)} {platform:<22}{msg}")

    # ── Footer
    print()
    print(sep)
    print(
        f"{indent}{_c(GREEN)}{_c(BOLD)}{len(results)}{_c(RESET)} websites checked in "
        f"{_c(BOLD)}{elapsed:.2f}{_c(RESET)} seconds  "
        f"{_c(DIM)}({len(taken)} found){_c(RESET)}"
    )
    print()
