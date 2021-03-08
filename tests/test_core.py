import re

from http import HTTPStatus

import aiohttp
import pytest
import responses

from quickbuild import AsyncQBClient, QBClient, QBError, QBProcessingError

GET_VERSION_DATA = '6.0.9'


@responses.activate
def test_sync_client():
    responses.add(
        responses.GET,
        re.compile(r'.*/rest/version'),
        body=GET_VERSION_DATA,
        status=200
    )

    try:
        client = QBClient(
            'http://server',
            'login',
            'password',
            timeout=10,
        )

        version = client.get_version()
        assert version.major == 6
        assert version.minor == 0
        assert version.patch == 9
    finally:
        client.close()


@responses.activate
def test_sync_client_retry():
    # responses library does`t support Retry mock
    # https://github.com/getsentry/responses/issues/135
    # so, just cover code of retry constructor
    client = QBClient(
        'http://server',
        'login',
        'password',
        retry=dict(
            total=10,
            factor=1,
            statuses=[400, 500],
        )
    )

    assert client.session.adapters['http://'].max_retries.status_forcelist == [400, 500]


@pytest.mark.asyncio
async def test_async_client(aiohttp_mock):
    try:
        client = AsyncQBClient(
            'http://server',
            'login',
            'password',
            timeout=10,
        )

        aiohttp_mock.get(
            'http://server/rest/version',
            body=GET_VERSION_DATA,
            status=200,
        )

        version = await client.get_version()
        assert version.major == 6
        assert version.minor == 0
        assert version.patch == 9
    finally:
        await client.close()


@pytest.mark.asyncio
async def test_async_client_retry(aiohttp_mock):
    client = AsyncQBClient(
        'http://server',
        'login',
        'password',
        retry=dict(
            total=10,
            statuses=[500],
        )
    )

    aiohttp_mock.get(
        'http://server/rest/version',
        body='Server error',
        status=500,
    )

    aiohttp_mock.get(
        'http://server/rest/version',
        body=GET_VERSION_DATA,
        status=200,
    )

    version = await client.get_version()
    assert version.major == 6
    assert version.minor == 0
    assert version.patch == 9
    await client.close()


@pytest.mark.asyncio
async def test_async_client_retry_exception(aiohttp_mock):
    client = AsyncQBClient(
        'http://server',
        'login',
        'password',
        retry=dict(
            total=2,
            statuses=[500],
        )
    )

    aiohttp_mock.get(
        'http://server/rest/version',
        exception=aiohttp.ClientError()
    )

    aiohttp_mock.get(
        'http://server/rest/version',
        exception=aiohttp.ClientError()
    )

    with pytest.raises(QBError):
        await client.get_version()

    await client.close()


@responses.activate
def test_pause_success():
    responses.add(
        responses.GET,
        re.compile(r'.*/rest/pause'),
        body='paused'
    )

    QBClient('http://server').pause()


@responses.activate
def test_pause_error():
    responses.add(
        responses.GET,
        re.compile(r'.*/rest/pause'),
        body='error'
    )

    with pytest.raises(QBError):
        QBClient('http://server').pause()


@responses.activate
def test_resume_success():
    responses.add(
        responses.GET,
        re.compile(r'.*/rest/resume'),
        body='resumed'
    )

    QBClient('http://server').resume()


@responses.activate
def test_resume_error():
    responses.add(
        responses.GET,
        re.compile(r'.*/rest/resume'),
        body='paused'
    )

    with pytest.raises(QBError):
        QBClient('http://server').resume()


@responses.activate
def test_get_pause_information_success():
    BODY = r"""<?xml version="1.0" encoding="UTF-8"?>

    <com.pmease.quickbuild.setting.system.PauseSystem>
      <user>admin</user>
    </com.pmease.quickbuild.setting.system.PauseSystem>
    """

    responses.add(
        responses.GET,
        re.compile(r'.*/rest/paused'),
        body=BODY
    )

    info = QBClient('http://server').get_pause_information()
    assert info['user'] == 'admin'


@responses.activate
def test_get_pause_information_error():
    responses.add(
        responses.GET,
        re.compile(r'.*/rest/paused'),
        status=HTTPStatus.NO_CONTENT,
    )

    with pytest.raises(QBProcessingError):
        QBClient('http://server').get_pause_information()
