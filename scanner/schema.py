from dataclasses import dataclass, field
from typing import Any

@dataclass
class ScanResult:
    label: str
    requested_symbol: str
    resolved_symbol: str | None
    timeframe: str
    available: bool
    data_status: str
    auction_state: str | None = None
    price: float | None = None
    vwap: float | None = None
    price_vs_vwap: str | None = None
    volume_expansion: bool | None = None
    volume_profile: dict[str, Any] = field(default_factory=dict)
    structure: dict[str, Any] = field(default_factory=dict)
    retest: dict[str, Any] = field(default_factory=dict)
    raw: dict[str, Any] = field(default_factory=dict)
    error: str | None = None

def empty_result(label: str, symbol: str, timeframe: str, error: str) -> ScanResult:
    return ScanResult(label, symbol, None, timeframe, False, "unavailable", error=error)
