"""Handshake MCP sungguhan (stdio) ke mcp-canva lalu panggil canva_browser_status, persis seperti Claude.
Pakai: .venv/Scripts/python.exe scripts/verify_browser_mcp.py"""
import asyncio
import json
import sys
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

EXE = Path(sys.executable).with_name("mcp-canva.exe")


async def main():
    async with stdio_client(StdioServerParameters(command=str(EXE))) as (r, w):
        async with ClientSession(r, w) as s:
            await s.initialize()
            names = [t.name for t in (await s.list_tools()).tools]
            print(f"[OK ] handshake, {len(names)} tool:", [n for n in names if "browser" in n])
            res = await s.call_tool("canva_browser_status", {})
            print("[OK ] canva_browser_status:", json.dumps(json.loads(res.content[0].text), ensure_ascii=False))


asyncio.run(main())
