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
def test_get_queue_id_by_name(client):
    responses.add(
        responses.GET,
        re.compile(r'.*/rest/ids'),
        content_type='application/text',
        body='1',
    )

    response = client.identifiers.get_queue_id_by_name('queue')
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


@responses.activate
def test_get_group_id_by_name(client):
    responses.add(
        responses.GET,
        re.compile(r'.*/rest/ids'),
        content_type='application/text',
        body='1',
    )

    response = client.groups.get_id_by_name('group')
    assert response == 1


@responses.activate
def test_get_build_id_by_request_id(client):
    responses.add(
        responses.GET,
        re.compile(r'.*/rest/ids'),
        content_type='application/text',
        body='2',
    )

    response = client.builds.get_id_by_request_id(1)
    assert response == 2


@responses.activate
def test_get_build_id_by_build_name(client):
    responses.add(
        responses.GET,
        re.compile(r'.*/rest/ids'),
        content_type='application/text',
        body='123',
    )

    response = client.builds.get_id_by_build_name('1.latest')
    assert response == 123


@responses.activate
def test_get_dashboard_id_by_dashboard_fqn(client):
    responses.add(
        responses.GET,
        re.compile(r'.*/rest/ids'),
        content_type='application/text',
        body='1',
    )

    response = client.dashboards.get_id_by_fqn('1.project1')
    assert response == 1
