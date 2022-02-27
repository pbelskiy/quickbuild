import re

import responses

AUTHORIZATIONS_XML = r"""<?xml version="1.0" encoding="UTF-8"?>

<list>
  <com.pmease.quickbuild.model.Authorization>
    <group>3</group>
    <configuration>3</configuration>
    <permissions>
      <string>RUN_BUILD</string>
      <string>STOP_BUILD</string>
    </permissions>
  </com.pmease.quickbuild.model.Authorization>
</list>
"""


@responses.activate
def test_get(client):
    responses.add(
        responses.GET,
        re.compile(r'.*/rest/authorizations'),
        content_type='application/xml',
        body=AUTHORIZATIONS_XML,
    )

    response = client.authorizations.get()
    assert len(response) == 1
    assert response[0]['group'] == 3
