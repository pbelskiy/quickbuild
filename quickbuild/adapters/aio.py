import asyncio

from typing import Any, Callable, Optional, Union

from aiohttp import (
    BasicAuth,
    ClientError,
    ClientResponse,
    ClientSession,
    ClientTimeout,
)

from quickbuild.core import QBError, QuickBuild, Response


class RetryClientSession:

    def __init__(self, loop: Optional[asyncio.AbstractEventLoop], options: dict):
        self.total = options.get('total') or 1
        self.factor = options.get('factor', 0)
        self.statuses = options.get('statuses', [])

        self.session = ClientSession(loop=loop)

    async def request(self, *args: Any, **kwargs: Any) -> ClientResponse:
        for total in range(self.total):
            try:
                response = await self.session.request(*args, **kwargs)
            except (ClientError, asyncio.TimeoutError) as e:
                if total + 1 == self.total:
                    raise QBError from e
            else:
                if response.status not in self.statuses:
                    break

            await asyncio.sleep(self.factor * (2 ** (total - 1)))

        return response

    async def close(self) -> None:
        await self.session.close()


class AsyncQBClient(QuickBuild):

    session = None  # type: Union[ClientSession, RetryClientSession]
    timeout = None

    def __init__(self,
                 url: str,
                 user: Optional[str] = None,
                 password: Optional[str] = None,
                 *,
                 loop: Optional[asyncio.AbstractEventLoop] = None,
                 verify: bool = True,
                 timeout: Optional[float] = None,
                 retry: Optional[dict] = None
                 ):
        """
        QuickBuild async client class.

        * url: ``str``
          Url of QuickBuild server, must include API version.

        * user: ``str`` (optional)
          User name, login.

        * password: ``str`` (optional)
          Password for user.

        * loop: ``AbstractEventLoop`` (optional)
          Asyncio current event loop.

        * verify: ``bool`` (optional)
          Verify SSL (default: true).

        * timeout: ``int``, (optional)
          HTTP request timeout.

        * retry: ``dict`` (optional)
          Retry options to prevent failures if server restarting or temporary
          network problem.

          - total: ``int`` Total retries count. (default 0)
          - factor: ``int`` Sleep between retries (default 0)
            {factor} * (2 ** ({number of total retries} - 1))
          - statuses: ``List[int]`` HTTP statues retries on. (default [])

          Example:

          .. code-block:: python

            retry = dict(
                attempts=10,
                factor=1,
                statuses=[500]
            )

        :returns: ``AsyncClient instance``
        :raises: ``QBError``
        """
        super().__init__()

        self.loop = loop or asyncio.get_event_loop()
        self.host = url

        self.auth = None
        if user and password:
            self.auth = BasicAuth(user, password)

        if retry:
            self.session = RetryClientSession(loop, retry)
        else:
            self.session = ClientSession(loop=self.loop)

        self.verify = verify

        if timeout:
            self.timeout = ClientTimeout(total=timeout)

    async def close(self) -> None:  # type: ignore
        await self.session.close()

    async def request(self,  # type: ignore
                      callback: Callable,
                      method: str,
                      path: str,
                      fcb: Optional[Callable] = None,
                      **kwargs: Any
                      ) -> str:

        if self.timeout and 'timeout' not in kwargs:
            kwargs['timeout'] = self.timeout

        response = await self.session.request(
            method,
            '{host}/rest/{path}'.format(
                host=self.host,
                path=path,
            ),
            auth=self.auth,
            ssl=self.verify,
            **kwargs
        )

        body = await response.text()
        return callback(Response(response.status, body), fcb)
