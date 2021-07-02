import re

import responses

AGENTS_UNAUTHORIZED_XML = r"""<?xml version="1.0" encoding="UTF-8"?>

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


@responses.activate
def test_get(client):
    responses.add(
        responses.GET,
        re.compile(r'.*/rest/buildagents/unauthorized'),
        content_type='application/xml',
        body=AGENTS_UNAUTHORIZED_XML,
    )

    response = client.agents.get_unauthorized()
    assert response[0]['ip'] == '172.17.0.1'
    assert response[0]['overSSL'] is False
