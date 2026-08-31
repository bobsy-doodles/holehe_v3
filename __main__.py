import argparse
import asyncio
import csv
import json
import sys
import time

from holehe_v2.core.loader  import load_validators
from holehe_v2.core.runner  import run_all
from holehe_v2.core.display import (
    print_banner, print_results, progress_bar, disable_colour
)


def parse_args():
    parser = argparse.ArgumentParser(
        prog="holehe_v2",
        description="Modern Day Email Intelligence & Reconnaissance Suite",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog=(
            "Examples:\n"
            "  python -m holehe_v2 target@email.com\n"
            "  python -m holehe_v2 target@email.com --only-used\n"
            "  python -m holehe_v2 target@email.com --json out.json\n"
            "  python -m holehe_v2 target@email.com --csv  out.csv\n"
            "  python -m holehe_v2 target@email.com -m flickr\n"
            "  python -m holehe_v2 target@email.com --proxy http://127.0.0.1:8080\n"
        ),
    )
    parser.add_argument("email",            help="Target email address to scan")
    parser.add_argument("--only-used",      action="store_true", help="Display only sites where the email is registered")
    parser.add_argument("--show-errors",    action="store_true", help="Show error messages next to [!] entries")
    parser.add_argument("--json",           metavar="FILE", dest="json_out", help="Export results to JSON file")
    parser.add_argument("--csv",            metavar="FILE", dest="csv_out",  help="Export results to CSV file")
    parser.add_argument("--no-colour",      action="store_true", help="Disable coloured output")
    parser.add_argument("-m", "--module",   metavar="NAME", dest="module", help="Scan a single module only (e.g. -m flickr)")
    parser.add_argument("--proxy",          metavar="URL", help="Proxy URL (e.g. http://127.0.0.1:8080)")
    parser.add_argument("-c", "--concurrency", type=int, default=50, metavar="N", help="Max concurrent requests (default: 50)")
    return parser.parse_args()


def _found(r) -> bool:
    return r.is_taken


def export_json(results, path: str) -> None:
    payload = {
        platform: {
            "exists":  _found(r),
            "url":     r.url,
            "message": r.message if r.is_error else None,
            "extra":   r.extra or None,
        }
        for platform, r in results.items()
    }
    with open(path, "w") as f:
        json.dump(payload, f, indent=2)
    print(f"[*] JSON saved to {path}")


def export_csv(results, path: str) -> None:
    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["platform", "exists", "url", "message", "extra"])
        for platform, r in sorted(results.items()):
            writer.writerow([
                platform,
                _found(r),
                r.url or "",
                r.message if r.is_error else "",
                json.dumps(r.extra) if r.extra else "",
            ])
    print(f"[*] CSV saved to {path}")

async def main() -> None:
    args = parse_args()

    if args.no_colour:
        disable_colour()

    print_banner()

    validators = load_validators()
    if not validators:
        print("[!] No modules found in modules/")
        sys.exit(1)

    if args.module:
        name = args.module.lower()
        if name not in validators:
            print(f"[!] Module '{name}' not found. Available: {', '.join(sorted(validators))}")
            sys.exit(1)
        validators = {name: validators[name]}

    total   = len(validators)
    results = {}

    start = time.monotonic()
    await asyncio.gather(
        run_all(args.email, validators, results, concurrency=args.concurrency, proxy=args.proxy),
        progress_bar(validators, results, total),
    )
    elapsed = time.monotonic() - start

    print_results(
        args.email,
        results,
        elapsed=elapsed,
        show_errors=args.show_errors,
        only_used=args.only_used,
    )

    if args.json_out:
        export_json(results, args.json_out)

    if args.csv_out:
        export_csv(results, args.csv_out)


if __name__ == "__main__":
    asyncio.run(main())
