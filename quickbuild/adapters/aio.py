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

        Args:
            url (str):
                Url of QuickBuild server, must include API version.

            user (Optional[str]):
                User name, login.

            password (Optional[str]):
                Password for user.

            loop (Optional[AbstractEventLoop]):
                Asyncio current event loop.

            verify (Optional[bool]):
                Verify SSL (default: true).

            timeout (Optional[int]):
                HTTP request timeout.

            retry (Optional[dict]):
                Retry options to prevent failures if server restarting or
                temporary network problem.

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

        Returns:
            AsyncClient instance
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

    async def _request(self,
                       method: str,
                       path: str,
                       *,
                       callback: Optional[Callable] = None,
                       **kwargs: Any
                       ) -> Any:

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

        result = self._process(
            Response(response.status, response.headers, body),
            callback
        )

        return result

    async def close(self) -> None:  # type: ignore
        """
        Close client session
        """
        await self.session.close()
