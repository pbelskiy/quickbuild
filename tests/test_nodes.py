import re

import responses


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
