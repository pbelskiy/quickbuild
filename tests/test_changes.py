import re

import responses


@responses.activate
def test_get_version(client):
    responses.add(
        responses.GET,
        re.compile(r'.*/rest/changes/version'),
        content_type='text/plain',
        body='3.2',
    )

    version = client.changes.get_version()
    assert version == '3.2'
