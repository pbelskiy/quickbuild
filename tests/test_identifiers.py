import re

import responses


@responses.activate
def test_get_resource_id_by_name(client):
    responses.add(
        responses.GET,
        re.compile(r'.*/rest/ids'),
        content_type='application/text',
        body='1',
    )

    response = client.identifiers.get_resource_id_by_name('root')
    assert response == 1


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


@responses.activate
def test_get_user_id_by_name(client):
    responses.add(
        responses.GET,
        re.compile(r'.*/rest/ids'),
        content_type='application/text',
        body='1',
    )

    response = client.users.get_id_by_name('admin')
    assert response == 1
