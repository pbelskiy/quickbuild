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


@responses.activate
def test_get_size(client):
    responses.add(
        responses.GET,
        re.compile(r'.*/rest/jira/size/.*'),
        content_type='text/plain',
        body='29',
    )

    size = client.issues.get_tracker('jira').get_size(
        'root/My/DEV',
        from_build=100,
        to_build=150,
    )

    assert size == 29
