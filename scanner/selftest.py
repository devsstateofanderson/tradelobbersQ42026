import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from config import SYMBOLS, TIMEFRAMES
from prompts import build_prompt
from codex_adapter import CodexTradingViewAdapter

def main():
    assert TIMEFRAMES == ("5m", "15m", "1h")
    labels = [s.label for s in SYMBOLS]
    assert labels == ["BTCUSD", "MBTC1!", "ETHUSD", "XRPUSD", "MNQ", "MCL", "MCC"]
    assert SYMBOLS[0].preferred == "COINBASE:BTCUSD"
    assert SYMBOLS[1].preferred == "CME:MBT"
    assert SYMBOLS[2].preferred == "COINBASE:ETHUSD"
    assert SYMBOLS[3].preferred == "COINBASE:XRPUSD"
    assert SYMBOLS[4].preferred == "CME:MNQ"
    assert SYMBOLS[5].preferred == "CME:MCL"
    assert SYMBOLS[6].preferred == "CME:MCC"
    payload = build_prompt(SYMBOLS, TIMEFRAMES)
    assert "Never invent" in payload
    assert "unfinished_high_low" in payload
    assert "volume_profile_context" in payload
    assert "u_v_tt_structure" in payload
    adapter = CodexTradingViewAdapter()
    assert adapter.codex_command
    print(json.dumps({"status":"ok","symbols":labels,"timeframes":list(TIMEFRAMES)}))

if __name__ == "__main__":
    main()
