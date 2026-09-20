from dataclasses import dataclass
import os

TIMEFRAMES = ("5m", "15m", "1h")

@dataclass(frozen=True)
class SymbolSpec:
    label: str
    preferred: str
    candidates: tuple[str, ...]

SYMBOLS = (
    SymbolSpec("BTCUSD", "COINBASE:BTCUSD", ("COINBASE:BTCUSD", "BTCUSD")),
    SymbolSpec("MBTC1!", "CME:MBT", ("CME:MBT", "CME:MBT1!", "MBTC1!")),
    SymbolSpec("ETHUSD", "COINBASE:ETHUSD", ("COINBASE:ETHUSD", "ETHUSD")),
    SymbolSpec("XRPUSD", "COINBASE:XRPUSD", ("COINBASE:XRPUSD", "XRPUSD")),
)

@dataclass(frozen=True)
class Settings:
    poll_seconds: int = int(os.getenv("TRADELOBBERS_POLL_SECONDS", "30"))
    codex_command: str = os.getenv("TRADELOBBERS_CODEX", "codex")
    tradingview_server_hint: str = os.getenv("TRADELOBBERS_TV_MCP", "tradingview")

SETTINGS = Settings()
