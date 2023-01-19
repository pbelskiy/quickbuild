from http import HTTPStatus

import aiohttp
import pytest

from quickbuild import AsyncQBClient, QBError

GET_VERSION_DATA = '6.0.9'


@pytest.mark.asyncio
async def test_client(aiohttp_mock):
    aiohttp_mock.get(
        'http://server/rest/version',
        content_type='text/plain',
        body=GET_VERSION_DATA,
        status=HTTPStatus.OK,
    )

    client = AsyncQBClient(
        'http://server',
        'user',
        'password',
        timeout=10,
    )

    version = await client.system.get_version()
    assert version.major == 6
    assert version.minor == 0
    assert version.patch == 9

    await client.close()


@pytest.mark.asyncio
async def test_client_retry(aiohttp_mock):
    aiohttp_mock.get(
        'http://server/rest/version',
        content_type='text/plain',
        body='Server error',
        status=HTTPStatus.INTERNAL_SERVER_ERROR,
    )

    aiohttp_mock.get(
        'http://server/rest/version',
        content_type='text/plain',
        body=GET_VERSION_DATA,
        status=HTTPStatus.OK,
    )

    client = AsyncQBClient(
        'http://server',
        'user',
        'password',
        retry=dict(
            total=10,
            statuses=[HTTPStatus.INTERNAL_SERVER_ERROR],
        )
    )

    version = await client.system.get_version()
    assert version.major == 6
    assert version.minor == 0
    assert version.patch == 9
    await client.close()

    with pytest.raises(QBError):
        AsyncQBClient('http://server', 'user', 'password', retry=dict(total=0))


@pytest.mark.asyncio
async def test_client_retry_exception(aiohttp_mock):
    aiohttp_mock.get(
        'http://server/rest/version',
        exception=aiohttp.ClientError()
    )

    aiohttp_mock.get(
        'http://server/rest/version',
        exception=aiohttp.ClientError()
    )

    client = AsyncQBClient(
        'http://server',
        'user',
        'password',
        retry=dict(
            total=2,
            statuses=[HTTPStatus.INTERNAL_SERVER_ERROR],
        )
    )

    with pytest.raises(QBError):
        await client.system.get_version()

    await client.close()


@pytest.mark.asyncio
async def test_update_auth_callback(aiohttp_mock):

    aiohttp_mock.get(
        'http://server/rest/version',
        content_type='text/plain',
        body=GET_VERSION_DATA,
        status=HTTPStatus.OK
    )

    aiohttp_mock.get(
        'http://server/rest/version',
        content_type='text/plain',
        body=GET_VERSION_DATA,
        status=HTTPStatus.UNAUTHORIZED
    )

    aiohttp_mock.get(
        'http://server/rest/version',
        content_type='text/plain',
        body=GET_VERSION_DATA,
        status=HTTPStatus.OK
    )

    async def callback():
        return 'login_new', 'password_new'

    client = AsyncQBClient(
        'http://server',
        'login_old',
        'password_old',
        auth_update_callback=callback
    )

    version = await client.system.get_version()
    assert version.major == 6
    assert client.auth.login == 'login_old'
    assert client.auth.password == 'password_old'

    version = await client.system.get_version()
    assert version.major == 6
    assert client.auth.login == 'login_new'
    assert client.auth.password == 'password_new'

    await client.close()
