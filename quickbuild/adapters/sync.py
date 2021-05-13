from typing import Any, Callable, Optional

from requests import Session
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from quickbuild.core import QuickBuild, Response


class QBClient(QuickBuild):

    def __init__(self,
                 url: str,
                 user: Optional[str] = None,
                 password: Optional[str] = None,
                 *,
                 verify: bool = True,
                 timeout: Optional[float] = None,
                 retry: Optional[dict] = None
                 ):
        """
        QuickBuild client class.

        Args:
            url (str):
                Url of QuickBuild server.

            user (Optional[str]):
                User name, login.

            password (Optional[str]):
                Password for user.

            verify (Optional[bool]):
                Verify SSL (default: true).

            timeout (Optional[float]):
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

        Returns:
            Client instance
        """
        super().__init__()

        self.host = url
        self.session = Session()

        if user and password:
            self.session.auth = (user, password)

        self.timeout = timeout
        self.verify = verify

        if not retry:
            return

        adapter = HTTPAdapter(max_retries=Retry(
            total=retry.get('total', 0),
            backoff_factor=retry.get('factor', 0),
            status_forcelist=retry.get('statuses', []),
            method_whitelist=['GET', 'POST', 'PATCH'],
        ))

        self.session.mount('http://', adapter)
        self.session.mount('https://', adapter)

    def _request(self,
                 method: str,
                 path: str,
                 *,
                 callback: Optional[Callable] = None,
                 **kwargs: Any
                 ) -> Any:

        if self.timeout and 'timeout' not in kwargs:
            kwargs['timeout'] = self.timeout

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

    def close(self) -> None:
        """
        Close client session
        """
        self.session.close()
