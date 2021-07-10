import re

import responses


@responses.activate
def test_get_configuration_id_by_path(client):
    responses.add(
        responses.GET,
        re.compile(r'.*/rest/ids'),
        content_type='application/text',
        body='1',
    )

    response = client.configurations.get_id_by_path('root')
    assert response == 1

