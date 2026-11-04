#!/usr/bin/env python3
"""NISTOR WoW V4: local WebSocket <-> AzerothCore TCP bridge.
Requires: python3 -m pip install websockets
Only loopback. Raw binary forwarding; does NOT implement SRP6 or WoW opcodes.
"""
import asyncio
import websockets

ROUTES = {"/auth": 3724, "/world": 8085}

async def handler(ws):
    path = ws.request.path.split("?", 1)[0]
    if path not in ROUTES:
        await ws.close(code=1008, reason="Unknown route")
        return
    port = ROUTES[path]
    try:
        reader, writer = await asyncio.wait_for(asyncio.open_connection("127.0.0.1", port), 3)
    except (OSError, TimeoutError):
        await ws.close(code=1011, reason="Upstream unavailable")
        return

    async def tcp_to_ws():
        while True:
            data = await reader.read(65536)
            if not data:
                break
            await ws.send(data)

    async def ws_to_tcp():
        async for data in ws:
            if not isinstance(data, bytes):
                await ws.close(code=1003, reason="Binary messages only")
                break
            writer.write(data)
            await writer.drain()

    tasks = [asyncio.create_task(tcp_to_ws()), asyncio.create_task(ws_to_tcp())]
    try:
        done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
        for task in pending:
            task.cancel()
        await asyncio.gather(*tasks, return_exceptions=True)
    finally:
        writer.close()
        try:
            await writer.wait_closed()
        except OSError:
            pass

async def main():
    async with websockets.serve(handler, "127.0.0.1", 8766, max_size=2**20,
                                origins=["http://127.0.0.1:8765", "http://localhost:8765"],
                                compression=None):
        print("NISTOR WoW V4 WebSocket proxy: ws://127.0.0.1:8766/auth and /world")
        print("Local only. Raw transport; authentication is not implemented.")
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
