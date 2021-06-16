import re

import aiohttp
import pytest
import responses

from quickbuild import AsyncQBClient, ContentType, QBClient, QBError

GET_VERSION_DATA = '6.0.9'


USERS_XML = """<?xml version="1.0" encoding="UTF-8"?>

<list>
  <com.pmease.quickbuild.model.User>
    <id>1</id>
    <favoriteDashboardIds>
      <long>1</long>
    </favoriteDashboardIds>
    <name>admin</name>
    <lastLogin>2021-06-10T14:18:21.292Z</lastLogin>
    <password secret="hash">0DPiKuNIrrVmD8IUCuw1hQxNqZc=</password>
    <pluginSettingDOMs/>
  </com.pmease.quickbuild.model.User>
  <com.pmease.quickbuild.model.User>
    <id>2</id>
    <favoriteDashboardIds/>
    <name>pbelskiy</name>
    <lastLogin>2021-06-07T14:24:49.066Z</lastLogin>
    <password secret="hash">je+glP0P8AYzGoaLZE16xTSJKC8=</password>
    <pluginSettingDOMs/>
  </com.pmease.quickbuild.model.User>
</list>
"""

USERS_JSON = """[ {
  "@class" : "com.pmease.quickbuild.model.User",
  "id" : 1,
  "favoriteDashboardIds" : [ 1 ],
  "name" : "admin",
  "lastLogin" : "2021-06-10T14:18:21.292+00:00",
  "password" : {
    "value" : "0DPiKuNIrrVmD8IUCuw1hQxNqZc=",
    "secret" : "hash"
  },
  "pluginSettingDOMs" : { }
}, {
  "@class" : "com.pmease.quickbuild.model.User",
  "id" : 2,
  "favoriteDashboardIds" : [ ],
  "name" : "pbelskiy",
  "lastLogin" : "2021-06-07T14:24:49.066+00:00",
  "password" : {
    "value" : "je+glP0P8AYzGoaLZE16xTSJKC8=",
    "secret" : "hash"
  },
  "pluginSettingDOMs" : { }
} ]
"""


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

        version = client.system.get_version()
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
            content_type='text/plain',
            body=GET_VERSION_DATA,
            status=200,
        )

        version = await client.system.get_version()
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
        content_type='text/plain',
        body='Server error',
        status=500,
    )

    aiohttp_mock.get(
        'http://server/rest/version',
        content_type='text/plain',
        body=GET_VERSION_DATA,
        status=200,
    )

    version = await client.system.get_version()
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
        await client.system.get_version()

    await client.close()


@responses.activate
def test_content_type_parse_get():
    responses.add(
        responses.GET,
        re.compile(r'.*/rest/users'),
        content_type='application/xml',
        body=USERS_XML,
        status=200,
    )

    client = QBClient('http://server', content_type=ContentType.PARSE)

    users = client.users.get()
    assert isinstance(users, list)


@responses.activate
def test_content_type_xml_get():
    responses.add(
        responses.GET,
        re.compile(r'.*/rest/users'),
        content_type='application/xml',
        body=USERS_XML,
        status=200,
    )

    client = QBClient('http://server', content_type=ContentType.XML)

    users = client.users.get()
    assert isinstance(users, str)


@responses.activate
def test_content_type_json_get():
    responses.add(
        responses.GET,
        re.compile(r'.*/rest/users'),
        content_type='application/json',
        body=USERS_JSON,
        status=200,
    )

    client = QBClient('http://server', content_type=ContentType.JSON)

    users = client.users.get()
    assert isinstance(users, list)


@responses.activate
def test_content_type_headers_sync_json_json():

    def callback(request):
        assert request.headers['Accept'] == 'application/json'
        return (200, request.headers, request.body)

    responses.add_callback(
        responses.GET,
        re.compile(r'.*/rest/memberships/\d+'),
        callback=callback
    )

    client = QBClient('http://server', content_type=ContentType.JSON)
    client.memberships.get_info(1)


@responses.activate
def test_content_type_headers_sync_xml_json():

    def callback(request):
        assert request.headers['Accept'] == 'application/json'
        return (200, request.headers, request.body)

    responses.add_callback(
        responses.GET,
        re.compile(r'.*/rest/memberships/\d+'),
        callback=callback
    )

    client = QBClient('http://server', content_type=ContentType.XML)
    client.memberships.get_info(1, content_type=ContentType.JSON)


@responses.activate
def test_content_type_headers_sync_json_xml():

    def callback(request):
        assert request.headers['Accept'] == '*/*'
        return (200, request.headers, request.body)

    responses.add_callback(
        responses.GET,
        re.compile(r'.*/rest/memberships/\d+'),
        callback=callback
    )

    client = QBClient('http://server', content_type=ContentType.JSON)
    client.memberships.get_info(1, content_type=ContentType.XML)
