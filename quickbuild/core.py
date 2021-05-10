import json

from abc import ABC, abstractmethod
from collections import namedtuple
from http import HTTPStatus
from typing import Any, Callable, Optional, Union

from quickbuild.endpoints import (
    Audits,
    Builds,
    Configurations,
    Groups,
    Requests,
    System,
    Tokens,
    Users,
)
from quickbuild.exceptions import (
    QBError,
    QBForbiddenError,
    QBNotFoundError,
    QBProcessingError,
)

Response = namedtuple('Response', ['status', 'headers', 'body'])


class QuickBuild(ABC):

    def __init__(self):
        self.audits = Audits(self)
        self.builds = Builds(self)
        self.configurations = Configurations(self)
        self.groups = Groups(self)
        self.requests = Requests(self)
        self.system = System(self)
        self.tokens = Tokens(self)
        self.users = Users(self)

    @staticmethod
    def _callback(response: Response, fcb: Optional[Callable] = None) -> Union[str, dict]:
        if response.status == HTTPStatus.NO_CONTENT:
            raise QBProcessingError(response.body)

        if response.status == HTTPStatus.NOT_FOUND:
            raise QBNotFoundError(response.body)

        if response.status == HTTPStatus.FORBIDDEN:
            raise QBForbiddenError(response.body)

        if response.status != HTTPStatus.OK:
            raise QBError(response.body)

        # native json from server
        if response.headers.get('Content-Type') == 'application/json':
            return json.loads(response.body)

        if fcb:
            return fcb(response.body)

        return response.body

    def _request(self,
                 method: str,
                 path: str,
                 *,
                 callback: Optional[Callable] = None,
                 **kwargs: Any
                 ) -> Any:
        return self._rest(self._callback, method, path, callback, **kwargs)

    @abstractmethod
    def _rest(self,
              callback: Callable,
              method: str,
              path: str,
              fcb: Optional[Callable] = None,
              **kwargs: Any
              ) -> Any:
        raise NotImplementedError

    @abstractmethod
    def close(self) -> None:
        raise NotImplementedError
