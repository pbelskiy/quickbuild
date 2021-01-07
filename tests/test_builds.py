import re

import pytest
import responses

from aioresponses import aioresponses

from quickbuild import AsyncQBClient, QBClient


@pytest.fixture
def aiohttp_mock():
    with aioresponses() as mock:
        yield mock


@responses.activate
def test_get_info():
    RESPONSE_DATA = r"""
    <?xml version="1.0" encoding="UTF-8"?>

    <com.pmease.quickbuild.model.Build>
      <id>1</id>
      <configuration>1</configuration>
      <version>1.0.0</version>
      <requester>1</requester>
      <scheduled>false</scheduled>
      <status>SUCCESSFUL</status>
      <statusDate>2021-01-06T19:59:52.752Z</statusDate>
      <beginDate>2021-01-06T19:59:52.617Z</beginDate>
      <duration>137</duration>
      <waitDuration>96</waitDuration>
      <stepRuntimes>
        <entry>
          <string>master</string>
          <com.pmease.quickbuild.stepsupport.StepRuntime>
            <status>SUCCESSFUL</status>
            <nodeAddress>5d94ceab5742:8810</nodeAddress>
            <resources/>
            <waitDuration>96</waitDuration>
            <duration>11</duration>
          </com.pmease.quickbuild.stepsupport.StepRuntime>
        </entry>
      </stepRuntimes>
      <repositoryRuntimes/>
      <secretAwareVariableValues/>
    </com.pmease.quickbuild.model.Build>
    """

    responses.add(
        responses.GET,
        re.compile(r'.*/rest/builds/\d+'),
        content_type='application/xml',
        body=RESPONSE_DATA,
    )

    client = QBClient('http://server', 'login', 'password')

    response = client.builds.get_info(1)

    assert '<id>1</id>' in response


@responses.activate
def test_get_status():
    RESPONSE_DATA = 'SUCCESS'

    responses.add(
        responses.GET,
        re.compile(r'.*/rest/builds/\d+/status'),
        body=RESPONSE_DATA,
    )

    client = QBClient('http://server', 'login', 'password')

    response = client.builds.get_status(1)

    assert response == RESPONSE_DATA


@responses.activate
def test_get_begin_date():
    RESPONSE_DATA = '1609963192617'  # 2021-01-06 22:59:52.617000

    responses.add(
        responses.GET,
        re.compile(r'.*/rest/builds/\d+/begin_date'),
        body=RESPONSE_DATA,
    )

    client = QBClient('http://server', 'login', 'password')

    response = client.builds.get_begin_date(1)

    assert response.year == 2021


@pytest.mark.asyncio
async def test_get_begin_date_async(aiohttp_mock):
    RESPONSE_DATA = '1609963192617'  # 2021-01-06 22:59:52.617000

    try:
        client = AsyncQBClient(
            'http://server',
            'login',
            'password',
        )

        aiohttp_mock.get(
            re.compile(r'.*/rest/builds/\d+/begin_date'),
            body=RESPONSE_DATA,
        )

        response = await client.builds.get_begin_date(1)
        assert response.year == 2021
    finally:
        await client.close()
