import re

import responses


@responses.activate
def test_get_version(client):
    responses.add(
        responses.GET,
        re.compile(r'.*/rest/junit/version'),
        content_type='text/plain',
        body='2.1',
    )

    version = client.reports.get_tracker('junit').get_version()
    assert version == '2.1'
