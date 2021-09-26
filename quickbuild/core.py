import json

from collections import namedtuple
from http import HTTPStatus
from inspect import signature
from typing import Any, Callable, Optional

from quickbuild.endpoints import (
    Agents,
    Audits,
    Builds,
    Configurations,
    Dashboards,
    Groups,
    Identifiers,
    Measurements,
    Memberships,
    Requests,
    Resources,
    Shares,
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

CONTENT_JSON = 'application/json'

Response = namedtuple('Response', ['status', 'headers', 'body'])


class QuickBuild:
    """
    NB: somehow using -H "Accept: application/json,application/xml,*/*" leads
    to server error.
    """
    def __init__(self, content_type: Optional[ContentType]):
        self._content_type = content_type

        self.agents = Agents(self)
        self.audits = Audits(self)
        self.builds = Builds(self)
        self.configurations = Configurations(self)
        self.dashboards = Dashboards(self)
        self.groups = Groups(self)
        self.identifiers = Identifiers(self)
        self.measurements = Measurements(self)
        self.memberships = Memberships(self)
        self.requests = Requests(self)
        self.resources = Resources(self)
        self.shares = Shares(self)
        self.system = System(self)
        self.tokens = Tokens(self)
        self.users = Users(self)

    def _get_headers(self, content_type: Optional[ContentType]) -> dict:
        headers = {}

        if content_type == ContentType.JSON or (
           self._content_type == ContentType.JSON and content_type is None):
            headers.update({
                'Accept': CONTENT_JSON,
                'Content-Type': CONTENT_JSON
            })

        return headers

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
        if response.headers.get('Content-Type') == CONTENT_JSON:
            return json.loads(response.body)

        if not callback:
            return response.body

        cb_parameters = signature(callback).parameters

        if 'content_type' in cb_parameters:
            if cb_parameters['content_type'].default is None or \
               cb_parameters['content_type'].default is cb_parameters['content_type'].empty:
                content_type = self._content_type
            else:
                content_type = cb_parameters['content_type'].default

            return callback(response.body, content_type=content_type)

        return callback(response.body)

    @staticmethod
    def _validate_retry_argument(retry: dict) -> None:
        for key in retry:
            if key not in ('total', 'factor', 'statuses'):
                raise QBError('Unknown key in retry argument: ' + key)

        if retry.get('total', 0) <= 0:
            raise QBError('Invalid `total` in retry argument must be > 0')

    @staticmethod
    def _validate_for_id(configuration: str) -> None:
        if '</id>' in configuration:
            raise QBError('`id` element must not be in XML for create method')

        try:
            data = json.loads(configuration)
        except json.JSONDecodeError:
            return

        if 'id' in data:
            raise QBError('`id` element must not be in JSON for create method')
