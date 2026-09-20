import argparse
import json
import sys
import time
from pathlib import Path

from config import SYMBOLS, TIMEFRAMES, SETTINGS
from codex_adapter import CodexTradingViewAdapter
from prompts import build_prompt

def print_header():
    print("\nTradeLobbers Live TradingView Scanner")
    print("Universe: " + " | ".join(s.label for s in SYMBOLS))
    print("Timeframes: " + " | ".join(TIMEFRAMES))
    print("Data policy: live TradingView MCP only; unavailable data is reported, never invented.")
    print("-" * 88)

def run_once(adapter):
    ok, detail = adapter.verify()
    if not ok:
        print(f"TRADINGVIEW MCP: UNAVAILABLE — {detail}", file=sys.stderr)
        return 2
    print("TRADINGVIEW MCP: CONNECTED")
    result = adapter.scan(build_prompt(SYMBOLS, TIMEFRAMES))
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    parser.add_argument("--once", action="store_true")
    args = parser.parse_args()
    Path(args.root).resolve()
    print_header()
    adapter = CodexTradingViewAdapter(SETTINGS.codex_command)
    while True:
        code = run_once(adapter)
        if args.once or code == 2:
            return code
        time.sleep(SETTINGS.poll_seconds)

if __name__ == "__main__":
    main()
