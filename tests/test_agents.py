import re

import responses

UNAUTHORIZED_AGENTS_XML = r"""<?xml version="1.0" encoding="UTF-8"?>

<list>
  <com.pmease.quickbuild.grid.UnauthorizedAgent>
    <ip>172.17.0.1</ip>
    <port>8811</port>
    <overSSL>false</overSSL>
    <hostName>live.local</hostName>
    <lastPulse>2021-07-02T21:20:19.393Z</lastPulse>
  </com.pmease.quickbuild.grid.UnauthorizedAgent>
</list>
"""

AGENTS_XML = r"""<?xml version="1.0" encoding="UTF-8"?>

<list>
  <com.pmease.quickbuild.model.Token>
    <id>1</id>
    <ip>172.17.0.1</ip>
    <port>8811</port>
    <test>false</test>
    <hostName>live.local</hostName>
    <offlineAlert>true</offlineAlert>
  </com.pmease.quickbuild.model.Token>
</list>
"""


@responses.activate
def test_get_active(client):
    responses.add(
        responses.GET,
        re.compile(r'.*/rest/buildagents/active'),
        content_type='application/xml',
        body=AGENTS_XML,
    )

    response = client.agents.get_active()
    assert response[0]['id'] == 1
    assert response[0]['ip'] == '172.17.0.1'


@responses.activate
def test_get_inactive(client):
    responses.add(
        responses.GET,
        re.compile(r'.*/rest/buildagents/inactive'),
        content_type='application/xml',
        body=AGENTS_XML,
    )

    response = client.agents.get_inactive()
    assert response[0]['id'] == 1
    assert response[0]['ip'] == '172.17.0.1'


@responses.activate
def test_get_unauthorized(client):
    responses.add(
        responses.GET,
        re.compile(r'.*/rest/buildagents/unauthorized'),
        content_type='application/xml',
        body=UNAUTHORIZED_AGENTS_XML,
    )

    response = client.agents.get_unauthorized()
    assert response[0]['ip'] == '172.17.0.1'
    assert response[0]['overSSL'] is False


@responses.activate
def test_get_running_steps(client):
    responses.add(
        responses.GET,
        re.compile(r'.*/rest/buildagents/.+/running_steps'),
        content_type='application/xml',
    )

    client.agents.get_running_steps('myagent:8811')
