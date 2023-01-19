from typing import Any, Callable, List, Optional, Tuple

from requests import Session
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from quickbuild.core import ContentType, QuickBuild, Response
from quickbuild.exceptions import QBError, QBUnauthorizedError


class QBClient(QuickBuild):

    def __init__(self,
                 url: str,
                 user: Optional[str] = None,
                 password: Optional[str] = None,
                 *,
                 content_type: ContentType = ContentType._DEFAULT,
                 verify: bool = True,
                 timeout: Optional[float] = None,
                 retry: Optional[dict] = None,
                 auth_update_callback: Optional[Callable[[], Tuple[str, str]]] = None
                 ) -> None:
        """
        QuickBuild client class.

        Args:
            url (str):
                URL of QuickBuild server.

            user (Optional[str]):
                User name.

            password (Optional[str]):
                Password for user.

            verify (Optional[bool]):
                Verify SSL (default: true).

            content_type (ContentType):
                How to process server content, get native XML as string, or
                parsing XML to Python types, or uses native JSON if QB10+ used.

            timeout (Optional[float]):
                HTTP request timeout.

            retry (Optional[dict]):
                Retry options to prevent failures if server restarting or
                temporary network problem. Disabled by default use total > 0
                to enable.

                - total: ``int`` Total retries count.
                - factor: ``int`` Sleep between retries (default 1)
                    {factor} * (2 ** ({number of total retries} - 1))
                - statuses: ``List[int]`` HTTP statues retries on. (default [])
                - methods: ``List[str]`` list of HTTP methods to retry, idempotent
                    methods are used by default.

                Example:

                .. code-block:: python

                    retry = dict(
                        total=10,
                        factor=1,
                        statuses=[500]
                    )

                With factor = 1

                ============  =============
                Retry number  Sleep
                ============  =============
                1              0.5 seconds
                2              1.0 seconds
                3              2.0 seconds
                4              4.0 seconds
                5              8.0 seconds
                6             16.0 seconds
                7             32.0 seconds
                8              1.1 minutes
                9              2.1 minutes
                10             4.3 minutes
                11             8.5 minutes
                12            17.1 minutes
                13            34.1 minutes
                14             1.1 hours
                15             2.3 hours
                16             4.6 hours
                17             9.1 hours
                18            18.2 hours
                19            36.4 hours
                20            72.8 hours
                ============  =============

            auth_update_callback (Optional[Callable[[], Tuple[str, str]]])
                Callback function which will be called on QBUnauthorizedError
                to update user and password and retry request again.

        Returns:
            Client instance
        """
        super().__init__(content_type)

        self.content_type = content_type
        self.host = url
        self.session = Session()

        if user and password:
            self.session.auth = (user, password)

        self.timeout = timeout
        self.verify = verify

        self.auth_update_callback = auth_update_callback

        if not retry:
            return

        self._validate_retry_argument(retry)
        adapter = HTTPAdapter(max_retries=Retry(
            total=retry['total'],
            backoff_factor=retry.get('factor', 1),
            status_forcelist=retry.get('statuses', []),
            method_whitelist=retry.get('methods', [
                'DELETE', 'GET', 'HEAD', 'OPTIONS', 'PUT', 'TRACE'
            ]),
        ))

        self.session.mount('http://', adapter)
        self.session.mount('https://', adapter)

    def _http_request(self,
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

        response = self.session.request(
            method,
            '{host}/rest/{path}'.format(
                host=self.host,
                path=path,
            ),
            verify=self.verify,
            **kwargs
        )

        result = self._process(
            Response(response.status_code, response.headers, response.text),
            callback
        )

        return result

    def _request(self, *args: Any, **kwargs: Any) -> Any:
        try:
            return self._http_request(*args, **kwargs)
        except QBUnauthorizedError:
            if self.auth_update_callback is None:
                raise

            user, password = self.auth_update_callback()
            self.session.auth = (user, password)
            return self._http_request(*args, **kwargs)

    @staticmethod
    def _chain(functions: List[Callable]) -> Any:
        """
        Helper function for creating call chain for functions.
        """
        prev = None

        for func in functions:
            try:
                prev = func(prev)

                while True:
                    if callable(prev):
                        prev = prev()
                    else:
                        break
            except QBError as e:
                prev = e

        return prev

    def close(self) -> None:
        """
        Close client session
        """
        self.session.close()
