from abc import ABC, abstractmethod
from collections import namedtuple
from http import HTTPStatus
from typing import Any, Callable

from quickbuild.exceptions import QuickBuildError

Response = namedtuple('Response', ['status', 'body'])


class QuickBuild(ABC):

    def __init__(self):
        ...

    @staticmethod
    def _callback(response: Response) -> str:
        if response.status != HTTPStatus.OK:
            raise QuickBuildError(response.body)

        return response.body

    @abstractmethod
    def close(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def request(self,
                callback: Callable[[Response], str],
                method: str,
                path: str,
                **kwargs: Any
                ) -> str:
        raise NotImplementedError

    def _request(self, method: str, path: str, **kwargs: Any) -> str:
        return self.request(self._callback, method, path, **kwargs)

    def get_version(self) -> str:
        """
        Show server version information.

        :returns: ``dict``
        :raises: ``QuickBuildError``
        """
        return self._request('GET', 'version')
