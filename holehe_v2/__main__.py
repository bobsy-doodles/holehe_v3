import argparse
import asyncio
import sys
from holehe_v2.api import EmailScanner

def main():
    parser = argparse.ArgumentParser(description="holehe_v2 — Next-Gen Email OSINT Scanner Engine")
    parser.add_argument("email", help="Target email identifier string to test")
    parser.add_argument("-m", "--module", help="Run scan on a single dedicated module name only", default=None)
    parser.add_argument("-c", "--concurrency", type=int, help="Maximum worker pooling requests threshold", default=50)
    parser.add_argument("--proxy", help="Route traffic using an intermediate proxy URL string", default=None)
    parser.add_argument("--only-used", action="store_true", help="Filter terminal interface feedback to show found hits only")
    args = parser.parse_args()

    scanner = EmailScanner(proxy=args.proxy, concurrency=args.concurrency)
    
    try:
        results = asyncio.run(scanner.scan(args.email, only_module=args.module))
    except Exception as e:
        print(f"Engine Core Runtime Critical Exception: {e}", file=sys.stderr)
        sys.exit(1)

    for result in results:
        if args.only_used and result.status != "[+]":
            continue
        print(result)

if __name__ == "__main__":
    main()
