import re

import aiohttp
import pytest
import responses

from aioresponses import aioresponses

from quickbuild import AsyncQBClient, QBClient, QuickBuildError

GET_VERSION_DATA = '6.0.9'


@pytest.fixture
def aiohttp_mock():
    with aioresponses() as mock:
        yield mock


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
        assert version == GET_VERSION_DATA
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
        assert version == GET_VERSION_DATA
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
    assert version == GET_VERSION_DATA
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

    with pytest.raises(QuickBuildError):
        await client.get_version()

    await client.close()
