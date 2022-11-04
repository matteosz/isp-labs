import websockets
import asyncio
import os
import hashlib

EMAIL = "your.email@epfl.ch"
PASSWORD = "correct horse battery staple"
N = int('EEAF0AB9ADB38DD69C33F80AFA8FC5E86072618775FF3C0B9EA2314C9C256576D674DF7496EA81D3383B4813D692C6E0E0D5D8E250B98BE48E495C1D6089DAD15DC7D7B46154D6B6CE8EF4AD69B15D4982559B297BCF1885C529F566660E57EC68EDBC3C05726CC02FD4CBF4976EAA9AFD5138FE8376435B9FC61D2FC0EB06E3', base=16)
g = 2
LENGTH = 32
url = "ws://127.0.0.1:5000"

async def run():
    async with websockets.connect(url) as websocket:

        await websocket.send(EMAIL)

        salt_hex = await websocket.recv()
        salt_bin = salt_hex.encode()

        a = int.from_bytes(os.urandom(LENGTH), "big")
        A = pow(g, a, N)
        A_hex = format(A, "x").encode()
        await websocket.send(A_hex)

        B_hex = await websocket.recv()
        B = int(B_hex, 16)

        h = hashlib.sha256()
        h.update(format(A, "x").encode)
        h.update(format(B, "x").encode)

        u_hex = h.hexdigest()
        u = int(u_hex, base=16)

        inner = hashlib.sha256()
        inner.update(EMAIL.encode())
        inner.update(b":")
        inner.update(PASSWORD.encode())

        outer = hashlib.sha256()
        outer.update(salt_bin)
        outer.update(inner.hexdigest().encode())

        x = int(outer.hexdigest(), 16)

        #S = (B - g^x)^(a + u * x) % N
        S = pow(B - pow(g, x, N), (a + u * x), N)

        h = hashlib.sha256()
        h.update("{0:b}".format(A))
        h.update("{0:b}".format(B))
        h.update("{0:b}".format(S))

        await websocket.send(h.hexdigest().encode())

        resp = await websocket.recv()
        print("Response: {}".format(resp))

asyncio.get_event_loop().run_until_complete(run())