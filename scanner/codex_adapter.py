import json
import subprocess
from typing import Any

class CodexTradingViewAdapter:
    def __init__(self, codex_command: str = "codex"):
        self.codex_command = codex_command

    def verify(self) -> tuple[bool, str]:
        try:
            version = subprocess.run([self.codex_command, "--version"], capture_output=True, text=True, timeout=10)
            if version.returncode != 0:
                return False, version.stderr.strip() or "codex --version failed"
            mcp = subprocess.run([self.codex_command, "mcp", "list"], capture_output=True, text=True, timeout=15)
            if mcp.returncode != 0:
                return False, mcp.stderr.strip() or "codex mcp list failed"
            output = (mcp.stdout + "\n" + mcp.stderr).strip()
            if "tradingview" not in output.lower():
                return False, "Codex is installed, but no TradingView MCP server was found in codex mcp list."
            return True, output
        except FileNotFoundError:
            return False, "Codex CLI not found. Install/configure Codex and its TradingView MCP server locally."
        except subprocess.TimeoutExpired:
            return False, "Timed out while verifying Codex/TradingView MCP."

    def scan(self, prompt: str) -> dict[str, Any]:
        cmd = [self.codex_command, "exec", "--skip-git-repo-check", "--json", prompt]
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        if proc.returncode != 0:
            raise RuntimeError(proc.stderr.strip() or "Codex scan failed")
        text = proc.stdout.strip()
        for line in reversed(text.splitlines()):
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                continue
            if isinstance(obj, dict):
                for key in ("result", "output", "text"):
                    value = obj.get(key)
                    if isinstance(value, dict):
                        return value
                    if isinstance(value, str):
                        try:
                            return json.loads(value)
                        except json.JSONDecodeError:
                            pass
        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise RuntimeError("Codex returned no parseable JSON scan result") from exc
