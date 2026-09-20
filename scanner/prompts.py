import json

SYSTEM_PROMPT = """You are the TradeLobbers TradingView data adapter.
Use ONLY live data actually returned by the connected TradingView MCP.
Never invent, estimate, backfill, or infer unavailable market data.
Resolve symbols through TradingView. Prefer COINBASE:BTCUSD, COINBASE:ETHUSD,
COINBASE:XRPUSD. For MBTC1!, investigate CME:MBT first.
Return ONLY valid JSON matching the requested schema.
"""

def build_prompt(symbols, timeframes):
    return SYSTEM_PROMPT + "\n\nRequest:\n" + json.dumps({
        "symbols": [{"label":s.label,"preferred":s.preferred,"candidates":list(s.candidates)} for s in symbols],
        "timeframes": list(timeframes),
        "fields": {
            "price": True, "vwap": True, "volume_expansion": True,
            "volume_profile_context": True, "weak_high_low": True,
            "strong_high_low": True, "u_v_tt_structure": True,
            "retests": True, "unfinished_high_low": True, "auction_context": True
        },
        "rules": [
            "If a symbol or timeframe is unavailable, mark available=false and explain data_status/error.",
            "Do not fabricate Volume Profile values if the MCP does not expose them.",
            "Distinguish observed data from derived structure classification.",
            "Return one result per symbol/timeframe."
        ]
    }, separators=(",", ":"))
