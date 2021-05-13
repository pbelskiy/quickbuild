import json

from collections import namedtuple
from http import HTTPStatus
from typing import Any, Callable, Optional

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


class QuickBuild:

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
    def _process(response: Response, callback: Optional[Callable] = None) -> Any:
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

        return callback(response.body)
