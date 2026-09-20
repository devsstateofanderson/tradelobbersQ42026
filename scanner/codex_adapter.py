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

    @staticmethod
    def _parse_json_object(value: Any) -> dict[str, Any] | None:
        if isinstance(value, dict):
            return value
        if not isinstance(value, str):
            return None
        candidate = value.strip()
        try:
            obj = json.loads(candidate)
            return obj if isinstance(obj, dict) else None
        except json.JSONDecodeError:
            # Be tolerant if the agent wrapped the JSON in markdown fences.
            if "{" in candidate and "}" in candidate:
                start = candidate.find("{")
                end = candidate.rfind("}") + 1
                try:
                    obj = json.loads(candidate[start:end])
                    return obj if isinstance(obj, dict) else None
                except json.JSONDecodeError:
                    return None
        return None

    def scan(self, prompt: str) -> dict[str, Any]:
        # --json is JSONL: stdout contains multiple JSON event objects, not one JSON document.
        # We therefore extract the final agent_message text and parse that as the scanner payload.
        cmd = [self.codex_command, "exec", "--skip-git-repo-check", "--json", prompt]
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        if proc.returncode != 0:
            raise RuntimeError(proc.stderr.strip() or "Codex scan failed")

        events: list[dict[str, Any]] = []
        for line in proc.stdout.splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                continue
            if isinstance(event, dict):
                events.append(event)

        # Prefer the last completed agent message, which is the final scanner response.
        for event in reversed(events):
            item = event.get("item")
            if not isinstance(item, dict):
                continue
            if item.get("type") != "agent_message":
                continue
            result = self._parse_json_object(item.get("text"))
            if result is not None:
                return result

        # Compatibility with alternate Codex event/output shapes.
        for event in reversed(events):
            for key in ("result", "output", "text"):
                result = self._parse_json_object(event.get(key))
                if result is not None:
                    return result

        raise RuntimeError(
            "Codex completed but returned no parseable JSON scanner result. "
            "See Codex stderr/output above for the underlying response."
        )
