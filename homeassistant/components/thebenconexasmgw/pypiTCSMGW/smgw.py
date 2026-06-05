import time

import aiohttp
import asyncio


class ConexaSmgwErr(Exception):
    """Base class to catch them all."""


class UnexpectedReturnCode(ConexaSmgwErr):
    """The smgw returned something the logic did not expect."""


# async def __anti_loop_middleware(request: aiohttp.ClientRequest, handler) -> aiohttp.ClientResponse:
#     # Track retries using a custom private attribute on the request object
#     if not hasattr(request, '_auth_attempts'):
#         request._auth_attempts = 0

#     response = await handler(request)

#     if response.status == 401:
#         request._auth_attempts += 1
#         # If we already retried once and we're getting a 401 again, kill the loop
#         if request._auth_attempts > 1:
#             print("Circuit breaker triggered: Invalid credentials provided.")
#             return response

#     return response


async def buildCompleteUrl(session: aiohttp.ClientSession, host, usr, pw) -> str:
    writer = None
    try:
        print(f"es ist {time.time()}")
        _, writer = await asyncio.wait_for(
            asyncio.open_connection( host, 443 ),
            timeout=3
        )
        print(f"Connected! {time.time()}")
    except asyncio.TimeoutError:
        print(f"Connection to {host} timed out after 3 seconds.")
    except Exception as e:
        print(f"Connection failed due to an error: {e}")
    finally:
        if writer:
            writer.close()
            await writer.wait_closed()

    async with session.post(
        f"https://{host}/smgw/m2m",
        ssl=False,
        headers={"content-type": "application/json"},
        allow_redirects=False,
        timeout=aiohttp.ClientTimeout(connect=6),
        middlewares=(aiohttp.DigestAuthMiddleware(login=usr, password=pw),),
    ) as response:
        if response.status != 307:
            txt = await response.text()
            raise UnexpectedReturnCode(
                f"SMGW should have returned 307 but instead it returned: {response.status} and following message: {txt}"
            )
        # print("Status:", response.status)
        # print("Content-type:", response.headers['content-type'])
        # print(f"elRedirect: {response.headers.get('Location')}!")
        # txt = await response.text()
        # print("Body:", txt, "...")
        return f"https://{host}{response.headers.get('Location')}"


class ConexaSMGW:
    def __init__(self, session: aiohttp.ClientSession, m2mUrl, usr, pw) -> None:
        print("ahahah")
        self.__m2mUrl = m2mUrl
        self.__usr = usr
        self.__pw = pw
        self.__session = session
        self.__m2mAddr = f"https://{self.__host}/smgw/m2m"
        self.__digest_auth = aiohttp.DigestAuthMiddleware(login=usr, password=pw)
        self.__default_post_kwargs = {
            "ssl": False,
            "headers": {"content-type": "application/json"},
            "allow_redirects": False,
            "middlewares": (self.__digest_auth,),
        }

    async def lol(self):
        print(f"hi {self.__usr}")
        await self._echt()

    async def _echt(self):
        print(f"going to post: {self.__m2mAddr}")
        async with self.__session.post(
            self.__m2mAddr, **self.__default_post_kwargs
        ) as response:
            print("Status:", response.status)
            print("Content-type:", response.headers["content-type"])
            print(f"elRedirect: {response.headers.get('Location')}!")
            html = await response.text()
            print("Body:", html, "...")
