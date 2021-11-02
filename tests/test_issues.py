import re

import responses


@responses.activate
def test_get_version(client):
    responses.add(
        responses.GET,
        re.compile(r'.*/rest/jira/version'),
        content_type='text/plain',
        body='3.1',
    )

    version = client.issues.get_tracker('jira').get_version()
    assert version == '3.1'
