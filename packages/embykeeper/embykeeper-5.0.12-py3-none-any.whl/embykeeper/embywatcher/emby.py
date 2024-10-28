import asyncio
import random
from urllib.parse import urlencode, urlunparse
import uuid
import warnings

import aiohttp
from aiohttp_socks import ProxyConnector, ProxyType

with warnings.catch_warnings():
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    from embypy.emby import Emby as _Emby
    from embypy.objects import EmbyObject
    from embypy.utils.asyncio import async_func
    from embypy.utils.connector import Connector as _Connector
from loguru import logger

from .. import __version__

logger = logger.bind(scheme="embywatcher")


class Connector(_Connector):
    """重写的 Emby 连接器, 以支持代理."""

    def __init__(
        self, url, proxy=None, ua=None, device=None, client=None, client_id=None, user_id=None, **kargs
    ):
        super().__init__(url, **kargs)
        self.proxy = proxy
        self.ua = ua
        self.device = device
        self.client = client
        self.client_id = client_id
        self.user_id = user_id
        self.fake_headers = self.get_fake_headers()
        self.watch = asyncio.create_task(self.watchdog())

    async def watchdog(self, timeout=60):
        logger.debug("Emby 链接池看门狗启动.")
        try:
            counter = {}
            while True:
                await asyncio.sleep(10)
                for s, u in self._session_uses.items():
                    try:
                        if u and u <= 0:
                            if s in counter:
                                counter[s] += 1
                                if counter[s] >= timeout / 10:
                                    logger.debug("销毁了 Emby Session")
                                    async with await self._get_session_lock():
                                        counter[s] = 0
                                        await self._sessions[s].close()
                                        self._sessions[s] = None
                                        self._session_uses[s] = None
                            else:
                                counter[s] = 1
                        else:
                            counter.pop(s, None)
                    except (TypeError, KeyError):
                        pass
        except asyncio.CancelledError:
            for s in self._sessions.values():
                if s:
                    try:
                        await asyncio.wait_for(s.close(), 1)
                    except asyncio.TimeoutError:
                        pass

    def get_device_uuid(self):
        rd = random.Random()
        rd.seed(uuid.getnode())
        return uuid.UUID(int=rd.getrandbits(128))

    def get_fake_headers(self):
        headers = {}
        ios_uas = [
            "CFNetwork/1335.0.3 Darwin/21.6.0",
            "CFNetwork/1406.0.4 Darwin/22.4.0",
            "CFNetwork/1333.0.4 Darwin/21.5.0",
        ]
        client = "Fileball" if not self.client else self.client
        device = "iPhone" if not self.device else self.device
        user_id = str(uuid.uuid4()).upper() if not self.user_id else self.user_id
        device_id = str(self.get_device_uuid()).upper() if not self.device_id else self.device_id
        version = f"1.2.{random.randint(0, 18)}"
        ua = f"Fileball/{random.choice([200, 233])} {random.choice(ios_uas)}" if not self.ua else self.ua
        auth_headers = {
            "UserId": user_id,
            "Client": client,
            "Device": device,
            "DeviceId": device_id,
            "Version": version,
        }
        auth_header = f"Emby {','.join([f'{k}={v}' for k, v in auth_headers.items()])}"
        if self.token:
            headers["X-Emby-Token"] = self.token
        headers["User-Agent"] = ua
        headers["X-Emby-Authorization"] = auth_header
        headers["Accept-Language"] = "zh-CN,zh-Hans;q=0.9"
        headers["Content-Type"] = "application/json"
        return headers

    async def _get_session(self):
        loop = asyncio.get_running_loop()
        loop_id = hash(loop)
        async with await self._get_session_lock():
            session = self._sessions.get(loop_id)
            if not session:
                if self.proxy:
                    connector = ProxyConnector(
                        proxy_type=ProxyType[self.proxy["scheme"].upper()],
                        host=self.proxy["hostname"],
                        port=self.proxy["port"],
                        username=self.proxy.get("username", None),
                        password=self.proxy.get("password", None),
                        verify_ssl=False,
                    )
                else:
                    connector = aiohttp.TCPConnector(verify_ssl=False)
                session = aiohttp.ClientSession(headers=self.fake_headers, connector=connector)
                self._sessions[loop_id] = session
                self._session_uses[loop_id] = 1
                logger.debug("创建了新的 Emby Session.")
            else:
                self._session_uses[loop_id] += 1
            return session

    async def _end_session(self):
        loop = asyncio.get_running_loop()
        loop_id = hash(loop)
        async with await self._get_session_lock():
            self._session_uses[loop_id] -= 1

    async def _get_session_lock(self):
        loop = asyncio.get_running_loop()
        return self._session_locks.setdefault(loop, asyncio.Lock())

    async def _reset_session(self):
        async with await self._get_session_lock():
            loop = asyncio.get_running_loop()
            loop_id = hash(loop)
            self._sessions[loop_id] = None
            self._session_uses[loop_id] = 0

    @async_func
    async def login_if_needed(self):
        if not self.token:
            return await self.login()

    @async_func
    async def _req(self, method, path, params={}, **query):
        query.pop("format", None)
        await self.login_if_needed()
        for i in range(self.tries):
            url = self.get_url(path, **query)
            try:
                params = {"timeout": self.timeout, **params}
                resp = await method(url, **params)
            except (aiohttp.ClientConnectionError, OSError, asyncio.TimeoutError) as e:
                logger.debug(f'连接 "{url}" 失败, 即将重连: {e.__class__.__name__}: {e}')
            else:
                if self.attempt_login and resp.status == 401:
                    raise aiohttp.ClientConnectionError("用户名密码错误")
                if await self._process_resp(resp):
                    return resp
            await asyncio.sleep(random.random() * i + 0.2)
        raise aiohttp.ClientConnectionError("无法连接到服务器.")

    @async_func
    async def get_stream_noreturn(self, path, **query):
        try:
            session = await self._get_session()
            async with await self._req(session.get, path, params={"timeout": 0}, **query) as resp:
                async for _ in resp.content.iter_any():
                    await asyncio.sleep(random.uniform(5, 10))
        finally:
            await self._end_session()

    def get_url(self, path="/", websocket=False, remote=True, userId=None, pass_uid=False, **query):
        userId = userId or self.userid
        if pass_uid:
            query["userId"] = userId

        if remote:
            url = self.urlremote or self.url
        else:
            url = self.url

        if websocket:
            scheme = url.scheme.replace("http", "ws")
        else:
            scheme = url.scheme

        url = urlunparse((scheme, url.netloc, path, "", "{params}", "")).format(
            UserId=userId, ApiKey=self.api_key, DeviceId=self.device_id, params=urlencode(query)
        )

        return url[:-1] if url[-1] == "?" else url


class Emby(_Emby):
    def __init__(self, url, **kw):
        """重写的 Emby 类, 以支持代理."""
        connector = Connector(url, **kw)
        EmbyObject.__init__(self, {"ItemId": "", "Name": ""}, connector)
        self._partial_cache = {}
        self._cache_lock = asyncio.Condition()

    @async_func
    async def get_items(
        self,
        types,
        path="/Users/{UserId}/Items",
        fields=None,
        limit=10,
        sort="SortName",
        ascending=True,
        **kw,
    ):
        if not fields:
            fields = ["Path", "ParentId", "Overview", "PremiereDate", "DateCreated"]
        resp = await self.connector.getJson(
            path,
            remote=False,
            format="json",
            recursive="true",
            includeItemTypes=",".join(types),
            fields=fields,
            sortBy=sort,
            sortOrder="Ascending" if ascending else "Descending",
            limit=limit,
            **kw,
        )
        return await self.process(resp)
