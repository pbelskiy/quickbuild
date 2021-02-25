
import re

import pytest
import responses

from quickbuild import AsyncQBClient, QBClient

TOKEN_XML = r"""<?xml version="1.0" encoding="UTF-8"?>

<list>
  <com.pmease.quickbuild.model.Token>
    <id>120204</id>
    <value>84858611-a1fe-4f88-a49c-f600cf0ecf11</value>
    <ip>192.168.1.100</ip>
    <port>8811</port>
    <test>false</test>
    <lastUsedDate>2021-02-08T20:01:09.426Z</lastUsedDate>
    <lastUsedReason>Run step (configuration: root/pipelineC, build: B.50906, step: master&gt;build)</lastUsedReason>
    <hostName>quickbuild-agent-192-168-1-100</hostName>
    <offlineAlert>true</offlineAlert>
  </com.pmease.quickbuild.model.Token>
</list>
"""

TOKENS_XML = r"""<?xml version="1.0" encoding="UTF-8"?>

<list>
  <com.pmease.quickbuild.model.Token>
    <id>117554</id>
    <value>bee7e8ff-fd9a-475a-8cf5-42a5353b8875</value>
    <ip>192.168.1.100</ip>
    <port>8811</port>
    <test>false</test>
    <lastUsedDate>2021-02-08T20:08:29.360Z</lastUsedDate>
    <lastUsedReason>Check build condition (configuration: root/pipelineA)</lastUsedReason>
    <hostName>quickbuild-agent-192-168-1-100</hostName>
    <offlineAlert>true</offlineAlert>
  </com.pmease.quickbuild.model.Token>
  <com.pmease.quickbuild.model.Token>
    <id>115672</id>
    <value>27350640-d9f9-4a10-96ae-b6ec8fee998b</value>
    <ip>192.168.1.101</ip>
    <port>8811</port>
    <test>false</test>
    <lastUsedDate>2021-02-08T20:01:10.175Z</lastUsedDate>
    <lastUsedReason>Run step (configuration: root/pipelineA, build: B.1234, step: master&gt;finalize)</lastUsedReason>
    <hostName>quickbuild-agent-192-168-1-101</hostName>
    <offlineAlert>true</offlineAlert>
  </com.pmease.quickbuild.model.Token>
  <com.pmease.quickbuild.model.Token>
    <id>116545</id>
    <value>8f604c48-b9f4-4bbe-847c-c073b2aebc81</value>
    <ip>192.168.1.102</ip>
    <port>8811</port>
    <test>false</test>
    <lastUsedDate>2021-02-08T20:01:10.013Z</lastUsedDate>
    <lastUsedReason>Run step (configuration: root/pipelineB, build: B.123, step: master&gt;publish)</lastUsedReason>
    <hostName>quickbuild-agent-192-168-1-102</hostName>
    <offlineAlert>true</offlineAlert>
  </com.pmease.quickbuild.model.Token>
</list>
"""

EMPTY_TOKEN_XML = r"""<?xml version="1.0" encoding="UTF-8"?>

<list/>
"""


@responses.activate
def test_authorize():
    RESPONSE_DATA = '120123'

    responses.add(
        responses.GET,
        re.compile(r'.*/rest/tokens/authorize'),
        content_type='text/plain',
        body=RESPONSE_DATA,
        match_querystring=True,
    )

    response = QBClient('http://server').tokens.authorize('192.168.1.100', 8811)
    assert response == RESPONSE_DATA

    response = QBClient('http://server').tokens.authorize('192.168.1.100')
    assert response == RESPONSE_DATA


@responses.activate
def test_unauthorize():
    RESPONSE_DATA = '120123'

    responses.add(
        responses.GET,
        re.compile(r'.*/rest/tokens/unauthorize'),
        content_type='text/plain',
        body=RESPONSE_DATA,
        match_querystring=True,
    )

    response = QBClient('http://server').tokens.unauthorize('192.168.1.100', 8811)
    assert response == RESPONSE_DATA

    response = QBClient('http://server').tokens.unauthorize('192.168.1.100')
    assert response == RESPONSE_DATA


@responses.activate
def test_token_and_agent_details():
    responses.add(
        responses.GET,
        re.compile(r'.*/rest/tokens\?address=quickbuild-agent-192-168-1-100%3A8811'),
        content_type='application/xml',
        body=TOKEN_XML
    )

    response = QBClient('http://server').tokens.get('quickbuild-agent-192-168-1-100:8811')
    assert len(response) == 1
    assert response[0]['id'] == '120204'


@responses.activate
def test_tokens_and_agent_details():
    responses.add(
        responses.GET,
        re.compile(r'.*/rest/tokens'),
        content_type='application/xml',
        body=TOKENS_XML,
    )

    response = QBClient('http://server').tokens.get()
    assert len(response) == 3
    assert response[0]['id'] == '117554'
    assert response[1]['id'] == '115672'
    assert response[2]['id'] == '116545'


@responses.activate
def test_tokens_and_agent_details_with_unknown_address():
    responses.add(
        responses.GET,
        re.compile(r'.*/rest/tokens\?address=unknown'),
        content_type='application/xml',
        body=EMPTY_TOKEN_XML,
        match_querystring=True,
    )

    response = QBClient('http://server').tokens.get('unknown')
    assert len(response) == 0
    assert response == []


@pytest.mark.asyncio
async def test_authorize_async(aiohttp_mock):
    RESPONSE_DATA = '120123'

    client = AsyncQBClient('http://server')
    try:
        aiohttp_mock.get(
            re.compile(r'.*/rest/tokens/authorize'),
            body=RESPONSE_DATA,
        )

        response = await client.tokens.authorize('192.168.1.100')
        assert response == RESPONSE_DATA
    finally:
        await client.close()


@pytest.mark.asyncio
async def test_unauthorize_async(aiohttp_mock):
    RESPONSE_DATA = '120123'

    client = AsyncQBClient('http://server')
    try:
        aiohttp_mock.get(
            re.compile(r'.*/rest/tokens/unauthorize'),
            body=RESPONSE_DATA,
        )

        response = await client.tokens.unauthorize('192.168.1.100')
        assert response == RESPONSE_DATA
    finally:
        await client.close()
