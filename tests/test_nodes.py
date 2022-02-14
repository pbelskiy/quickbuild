import re

import responses

ATTRIBUTES_DATA = r"""
<linked-hash-map>
  <entry>
    <string>attribute1</string>
    <string>value1</string>
  </entry>
  <entry>
    <string>attribute2</string>
    <string>value2</string>
  </entry>
</linked-hash-map>
"""


@responses.activate
def test_get_system_attributes(client):
    responses.add(
        responses.GET,
        re.compile(r'.*/rest/system_attributes/.+'),
        content_type='text/xml',
        body='',
    )

    # TODO: mock with some response
    client.nodes.get_system_attributes('agent:8811')


@responses.activate
def test_get_user_attributes(client):
    responses.add(
        responses.GET,
        re.compile(r'.*/rest/user_attributes/.+'),
        content_type='text/xml',
        body='',
    )

    # TODO: mock with some response
    client.nodes.get_user_attributes('agent:8811')


@responses.activate
def test_set_user_attributes(client):
    responses.add(
        responses.POST,
        re.compile(r'.*/rest/user_attributes/.+'),
        body=ATTRIBUTES_DATA,
    )

    client.nodes.set_user_attributes('agent:8811', ATTRIBUTES_DATA)
