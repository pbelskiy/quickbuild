from abc import ABC, abstractmethod
from collections import namedtuple
from http import HTTPStatus
from typing import Any, Callable, NamedTuple, Optional

import xmltodict

from quickbuild.endpoints.audits import Audits
from quickbuild.endpoints.builds import Builds
from quickbuild.endpoints.groups import Groups
from quickbuild.endpoints.tokens import Tokens
from quickbuild.endpoints.users import Users
from quickbuild.exceptions import (
    QBError,
    QBForbidden,
    QBNotFoundError,
    QBProcessingError,
)

Response = namedtuple('Response', ['status', 'body'])

ServerVersion = NamedTuple(
    'ServerVersion', [('major', int), ('minor', int), ('patch', int)]
)


class QuickBuild(ABC):

    def __init__(self):
        self.audits = Audits(self)
        self.builds = Builds(self)
        self.groups = Groups(self)
        self.tokens = Tokens(self)
        self.users = Users(self)

    @staticmethod
    def _callback(response: Response, fcb: Optional[Callable] = None) -> str:
        if response.status == HTTPStatus.NO_CONTENT:
            raise QBProcessingError(response.body)

        if response.status == HTTPStatus.NOT_FOUND:
            raise QBNotFoundError(response.body)

        if response.status == HTTPStatus.FORBIDDEN:
            raise QBForbidden(response.body)

        if response.status != HTTPStatus.OK:
            raise QBError(response.body)

        if fcb:
            return fcb(response.body)

        return response.body

    @abstractmethod
    def close(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def request(self,
                callback: Callable,
                method: str,
                path: str,
                fcb: Optional[Callable] = None,
                **kwargs: Any
                ) -> Any:
        raise NotImplementedError

    def _request(self,
                 method: str,
                 path: str,
                 fcb: Optional[Callable] = None,
                 **kwargs: Any
                 ) -> Any:
        return self.request(self._callback, method, path, fcb, **kwargs)

    def get_version(self) -> ServerVersion:
        """
        Show server version information.

        Returns:
            ServerVersion: NamedTuple with major, minor and patch version.
        """
        def callback(response: str) -> ServerVersion:
            return ServerVersion(*map(int, response.split('.')))

        return self._request('GET', 'version', callback)

    def pause(self) -> None:
        """
        Pause system.

        Raises:
            QBError: if system haven`t paused.
        """
        def callback(response: str) -> None:
            if response != 'paused':
                raise QBError(response)

        return self._request('GET', 'pause', callback)

    def resume(self) -> None:
        """
        Resumed system.

        Raises:
            QBError: if system haven`t resumed.
        """
        def callback(response: str) -> None:
            if response != 'resumed':
                raise QBError(response)

        return self._request('GET', 'resume', callback)

    def get_pause_information(self) -> None:
        """
        Get system pause information including pause reason.

        Returns:
            ServerVersion: NamedTuple with major, minor and patch version.

        Raises:
            QBProcessingError: will be raised if system is not paused.
        """
        def callback(response: str) -> None:
            root = xmltodict.parse(response)
            return root['com.pmease.quickbuild.setting.system.PauseSystem']

        return self._request('GET', 'paused', callback)
