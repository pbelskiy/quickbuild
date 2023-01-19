import re

from http import HTTPStatus

import pytest
import responses

from quickbuild import QBClient, QBError

GET_VERSION_DATA = '6.0.9'


@responses.activate
def test_client():
    responses.add(
        responses.GET,
        re.compile(r'.*/rest/version'),
        body=GET_VERSION_DATA,
    )

    try:
        client = QBClient(
            'http://server',
            'user',
            'password',
            timeout=10,
        )

        version = client.system.get_version()
        assert version.major == 6
        assert version.minor == 0
        assert version.patch == 9
    finally:
        client.close()


@responses.activate
def test_client_retry():
    # responses library does`t support Retry mock
    # https://github.com/getsentry/responses/issues/135
    # so, just cover code of retry constructor
    statuses = [HTTPStatus.BAD_REQUEST, HTTPStatus.INTERNAL_SERVER_ERROR]

    client = QBClient(
        'http://server',
        'user',
        'password',
        retry=dict(
            total=10,
            factor=1,
            statuses=statuses,
        )
    )

    assert client.session.adapters['http://'].max_retries.status_forcelist == statuses

    with pytest.raises(QBError):
        QBClient('http://server', retry=dict(total=1, strange_argument=1))


@responses.activate
def test_update_auth_callback():

    def callback():
        return 'login_new', 'password_new'

    responses.add(
        responses.GET,
        re.compile(r'.*/rest/version'),
        body=GET_VERSION_DATA,
        status=HTTPStatus.OK
    )

    responses.add(
        responses.GET,
        re.compile(r'.*/rest/version'),
        body=GET_VERSION_DATA,
        status=HTTPStatus.UNAUTHORIZED
    )

    responses.add(
        responses.GET,
        re.compile(r'.*/rest/version'),
        body=GET_VERSION_DATA,
        status=HTTPStatus.OK
    )

    client = QBClient(
        'http://server',
        'login_old',
        'password_old',
        auth_update_callback=callback
    )

    version = client.system.get_version()
    assert version.major == 6
    assert client.session.auth == ('login_old', 'password_old')

    version = client.system.get_version()
    assert version.major == 6
    assert client.session.auth == ('login_new', 'password_new')

    client.close()
