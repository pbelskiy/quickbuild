import asyncio

from typing import Any, Callable, List, Optional, Union

from aiohttp import (
    BasicAuth,
    ClientError,
    ClientResponse,
    ClientSession,
    ClientTimeout,
)

from quickbuild.core import ContentType, QuickBuild, Response
from quickbuild.exceptions import QBError


class RetryClientSession:

    def __init__(self, options: dict) -> None:
        self.total = options['total']
        self.factor = options.get('factor', 1)
        self.statuses = options.get('statuses', [])
        self.methods = options.get('methods', [
            'DELETE', 'GET', 'HEAD', 'OPTIONS', 'PUT', 'TRACE'
        ])

        self.session = ClientSession()

    async def request(self, *args: Any, **kwargs: Any) -> ClientResponse:
        for total in range(self.total):
            try:
                response = await self.session.request(*args, **kwargs)
            except (ClientError, asyncio.TimeoutError) as e:
                if total + 1 == self.total:
                    raise QBError from e
            else:
                if response.method.upper() not in self.methods:
                    break
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
                 content_type: Optional[ContentType] = ContentType._DEFAULT,
                 verify: bool = True,
                 timeout: Optional[float] = None,
                 retry: Optional[dict] = None
                 ) -> None:
        """
        QuickBuild async client class.

        Args:
            url (str):
                URL of QuickBuild server, must include API version.

            user (Optional[str]):
                User name.

            password (Optional[str]):
                Password for user.

            content_type (Optional[ContentType]):
                How to process server content, get native XML as string, or
                parsing XML to Python types, or uses native JSON if QB10+ used.

            verify (Optional[bool]):
                Verify SSL (default: true).

            timeout (Optional[int]):
                HTTP request timeout.

            retry (Optional[dict]):
                Retry options to prevent failures if server restarting or
                temporary network problem. Disabled by default use total > 0
                to enable.

                - total: ``int`` Total retries count.
                - factor: ``int`` Sleep between retries (default 1)
                    {factor} * (2 ** ({number of total retries} - 1))
                - statuses: ``List[int]`` HTTP statues retries on. (default [])
                - methods: ``List[str]`` list of HTTP methods to retry, udempotent
                    methods are used by default.

                Example:

                .. code-block:: python

                    retry = dict(
                        total=10,
                        factor=1,
                        statuses=[500]
                    )

        Returns:
            AsyncClient instance
        """
        super().__init__(content_type)

        self.content_type = content_type
        self.host = url

        self.auth = None
        if user and password:
            self.auth = BasicAuth(user, password)

        if retry:
            self._validate_retry_argument(retry)
            self.session = RetryClientSession(retry)
        else:
            self.session = ClientSession()

        self.verify = verify

        if timeout:
            self.timeout = ClientTimeout(total=timeout)

    async def _request(self,
                       method: str,
                       path: str,
                       *,
                       callback: Optional[Callable] = None,
                       content_type: Optional[ContentType] = None,
                       **kwargs: Any
                       ) -> Any:

        if self.timeout and 'timeout' not in kwargs:
            kwargs['timeout'] = self.timeout

        kwargs.setdefault('headers', {})
        kwargs['headers'].update(self._get_headers(content_type))

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

    @staticmethod
    async def _chain(functions: List[Callable]) -> Any:
        """
        Helper function for creating call chain of async and sync functions.
        """
        prev = None

        for func in functions:
            try:
                prev = func(prev)

                while True:
                    if asyncio.iscoroutine(prev):
                        prev = await prev  # type: ignore
                    elif callable(prev):
                        prev = prev()
                    else:
                        break
            except QBError as e:
                prev = e

        return prev

    async def close(self) -> None:  # type: ignore
        """
        Close client session
        """
        await self.session.close()
