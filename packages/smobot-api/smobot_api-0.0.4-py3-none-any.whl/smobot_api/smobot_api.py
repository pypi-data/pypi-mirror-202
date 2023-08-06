import aiohttp
import asyncio


class smobot_api:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self._base_url = f"https://mysmobot.com/secureapi/"
        self._headers = {
            "Accept-Encoding": "gzip, deflate",
            "User-Agent": "okhttp/3.6.0",
            "Connection": "close",
            "Content-Type": "application/json; charset=utf-8",
            "Accept-Language": "en-us",
        }
        cookies = {}
        self.session = aiohttp.ClientSession(cookies=cookies)

    async def close(self):
        await self.session.close()

    async def login(self):
        path = "login"
        body = {"username": self.username, "password": self.password}
        async with self.session.post(
            self._base_url + path, json=body, headers=self._headers
        ) as response:
            resp = await response.json()
            cookies = response.cookies
            response.raise_for_status()
            self._headers["X-Auth-Token"] = resp["access_token"]

    async def setpoint(self, serial, temp):
        path = f"smobot/setpoint"
        body = {
            "smobot": serial,
            "setpoint": temp
        }
        resp = await self.post(path, body)
        print(resp)
        status = await self.status(serial)
        print(status['setPoint'])


    async def status(self, serial):
        path = f"current/{serial}"
        return await self.get(path)

    @property
    async def serials(self):
        path = f"accounts/me"
        resp = await self.get(path)
        return [s['id'] for s in resp['smobots']]

    async def get(self, path):
        async with self.session.get(self._base_url + path, headers=self._headers) as response:
            return await response.json()

    async def post(self, path, body):
        async with self.session.post(self._base_url + path, json=body, headers=self._headers) as response:
            return await response.json()