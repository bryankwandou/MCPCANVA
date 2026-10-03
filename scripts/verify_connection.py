"""Prove the MCP server really talks to Canva.

Starts `creative-mcp` as a real MCP server over stdio, connects with the official
MCP client, and calls tools exactly like Claude does. Run on YOUR computer:

    python scripts/verify_connection.py            # read-only checks
    python scripts/verify_connection.py --write    # also creates a test design + test CapCut project
"""
import asyncio
import json
import os
import sys
import time

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

WRITE = "--write" in sys.argv


def show(title, ok, detail):
    print(f"[{'OK ' if ok else 'GAGAL'}] {title}")
    if detail:
        print("       " + str(detail)[:400].replace("\n", "\n       "))


async def call(s, name, args=None):
    r = await s.call_tool(name, args or {})
    texts = [c.text for c in r.content if getattr(c, "text", None)]
    if getattr(r, "structuredContent", None) and "result" in r.structuredContent:
        return (not r.isError), r.structuredContent["result"]
    try:  # a list result arrives as one content block per item
        data = [json.loads(t) for t in texts] if len(texts) > 1 else json.loads(texts[0]) if texts else None
    except ValueError:
        data = "".join(texts)
    return (not r.isError), data


async def main():
    params = StdioServerParameters(command=sys.executable, args=["-m", "creative_mcp.server"], env=dict(os.environ))
    async with stdio_client(params) as (r, w), ClientSession(r, w) as s:
        info = await s.initialize()
        tools = (await s.list_tools()).tools
        show("Handshake MCP", True, f"server={info.serverInfo.name}, {len(tools)} tool")

        ok, me = await call(s, "canva_whoami")
        name = me.get("profile", {}).get("profile", {}).get("display_name") if ok and isinstance(me, dict) else None
        show("Canva: akun terhubung", ok and bool(name), f"nama={name}" if name else me)
        if ok and name:
            ok2, ds = await call(s, "canva_list_designs", {"refresh": True})
            items = ds.get("items", []) if isinstance(ds, dict) else []
            show("Canva: daftar desain", ok2, [d.get("title") for d in items[:5]])
            if WRITE:
                ok3, d = await call(s, "canva_create_design", {"title": f"Tes MCP {time.strftime('%H:%M:%S')}", "preset": "presentation"})
                show("Canva: buat desain baru", ok3, d.get("design", {}).get("urls", {}).get("edit_url") if isinstance(d, dict) else d)



asyncio.run(main())
