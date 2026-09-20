# TradeLobbers Q4 2026

AI-native trading operating system and Mac live scanner.

## Single source of truth

This repository is the source of truth for the TradeLobbers Q4 2026 scanner. The Mac launcher pulls main before every run; do not maintain a second scanner implementation in an old local copy.

## Live scanner

The launcher command is:

    tradelobbers

It clones or hard-resets the local checkout to origin/main, verifies Python, verifies the local Codex CLI and TradingView MCP configuration, requests live TradingView data through the local Codex to TradingView MCP bridge, and scans BTCUSD, MBTC1!, ETHUSD, XRPUSD, MNQ, MCL and MCC on 5m, 15m, 1h and 4h.

Unavailable symbols or fields are reported explicitly. No market data is invented.

### Universe

- BTCUSD: prefer COINBASE:BTCUSD
- MBTC1!: investigate CME:MBT first, then CME:MBT1! and MBTC1!
- ETHUSD: prefer COINBASE:ETHUSD
- XRPUSD: prefer COINBASE:XRPUSD
- MNQ: prefer CME:MNQ
- MCL: prefer CME:MCL
- MCC: prefer CME:MCC

For CME symbols, TradingView resolves the requested contract/feed. Candidate fallbacks are retained for continuous-contract naming differences. If a requested symbol is unavailable, the scanner reports it rather than substituting fabricated data.

Symbol resolution is performed by TradingView.

### Timeframes

- 5m
- 15m
- 1h
- 4h

The 4h timeframe is part of the standard scanner context.

## TradeLobbers framework

The live request covers Volume Profile context, VWAP, price versus VWAP, volume expansion, Weak High / Weak Low, Strong High / Strong Low, U / V / TT structure, retests, unfinished highs/lows, and auction/context state.

The scanner never fabricates Volume Profile values or other unavailable data.

## Local prerequisites

- macOS
- Git
- Python 3
- Codex CLI
- TradingView MCP configured in the local Codex configuration

No TradingView credentials, OAuth tokens, API keys, or MCP secrets belong in this repository.

## Installation

    git clone https://github.com/devsstateofanderson/tradelobbersQ42026.git ~/TradeLobbers_Q4_2026
    chmod +x ~/TradeLobbers_Q4_2026/tradelobbers
    sudo ln -sf ~/TradeLobbers_Q4_2026/tradelobbers /usr/local/bin/tradelobbers

Then:

    tradelobbers

For one connectivity/data cycle:

    tradelobbers --once

Optional environment variables:

- TRADELOBBERS_ROOT: local checkout path
- TRADELOBBERS_CODEX: Codex executable name/path
- TRADELOBBERS_TV_MCP: local TradingView server hint
- TRADELOBBERS_POLL_SECONDS: scan interval, default 30 seconds

## Architecture

    tradelobbers
        |
    git fetch/reset origin/main
        |
    scanner/cli.py
        |
    Codex CLI (local)
        |
    TradingView Official MCP (local)
        |
    live symbol/timeframe data
        |
    TradeLobbers context JSON
