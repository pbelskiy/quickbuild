import re

import responses

RESOURCES_XML = r"""<?xml version="1.0" encoding="UTF-8"?>

<list>
</list>
"""


@responses.activate
def test_get(client):
    responses.add(
        responses.GET,
        re.compile(r'.*/rest/resources'),
        content_type='application/xml',
        body=RESOURCES_XML,
    )

    response = client.resources.get()
    assert len(response) == 0
