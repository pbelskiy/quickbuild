import json

from collections import namedtuple
from http import HTTPStatus
from inspect import signature
from typing import Any, Callable, Optional

from quickbuild.endpoints import (
    Audits,
    Builds,
    Configurations,
    Groups,
    Memberships,
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
    QBServerError,
)
from quickbuild.helpers import ContentType

Response = namedtuple('Response', ['status', 'headers', 'body'])


class QuickBuild:
    """
    NB: somehow using -H "Accept: application/json,application/xml,*/*" leads
    to server error.
    """
    def __init__(self, content_type: Optional[ContentType]):
        self._content_type = content_type

        self.audits = Audits(self)
        self.builds = Builds(self)
        self.configurations = Configurations(self)
        self.groups = Groups(self)
        self.memberships = Memberships(self)
        self.requests = Requests(self)
        self.system = System(self)
        self.tokens = Tokens(self)
        self.users = Users(self)

    def _process(self, response: Response, callback: Optional[Callable] = None) -> Any:
        if response.status == HTTPStatus.INTERNAL_SERVER_ERROR:
            raise QBServerError('JSON is supported by QB10+\n\n' + response.body)

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

        if not callback:
            return response.body

        if 'content_type' in signature(callback).parameters:
            return callback(response.body, content_type=self._content_type)

        return callback(response.body)
