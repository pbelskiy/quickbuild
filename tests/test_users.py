import re

import responses

USERS_XML = r"""<?xml version="1.0" encoding="UTF-8"?>

<list>
  <com.pmease.quickbuild.model.User>
    <id>1</id>
    <favoriteDashboardIds>
      <long>1</long>
    </favoriteDashboardIds>
    <name>admin</name>
    <password secret="hash">0DPiKuNIrrVmD8IUCuw1hQxNqZc=</password>
    <pluginSettingDOMs/>
  </com.pmease.quickbuild.model.User>
</list>
"""

USER_INFO_XML = """<?xml version="1.0" encoding="UTF-8"?>

<com.pmease.quickbuild.model.User>
  <id>1</id>
  <favoriteDashboardIds>
    <long>1</long>
  </favoriteDashboardIds>
  <name>admin</name>
  <password secret="hash">0DPiKuNIrrVmD8IUCuw1hQxNqZc=</password>
  <pluginSettingDOMs/>
</com.pmease.quickbuild.model.User>
"""


@responses.activate
def test_get(client):
    responses.add(
        responses.GET,
        re.compile(r'.*/rest/users'),
        content_type='application/xml',
        body=USERS_XML,
    )

    response = client.users.get()
    assert len(response) == 1
    assert response[0]['id'] == 1


@responses.activate
def test_get_info(client):
    responses.add(
        responses.GET,
        re.compile(r'.*/rest/users/1'),
        content_type='application/xml',
        body=USER_INFO_XML,
    )

    response = client.users.get_info(1)
    assert response['id'] == 1
    assert response['name'] == 'admin'


@responses.activate
def test_get_display_name(client):
    responses.add(
        responses.GET,
        re.compile(r'.*/rest/users/1/display_name'),
        content_type='application/xml',
        body='admin',
    )

    response = client.users.get_display_name(1)
    assert response == 'admin'


@responses.activate
def test_update(client):
    responses.add(
        responses.POST,
        re.compile(r'.*/rest/users'),
        body='1',
    )

    response = client.users.update(USER_INFO_XML)
    assert response == 1


@responses.activate
def test_create(client):
    responses.add(
        responses.POST,
        re.compile(r'.*/rest/users'),
        body='1',
    )

    response = client.users.create(USER_INFO_XML)
    assert response == 1


@responses.activate
def test_delete(client):
    responses.add(
        responses.DELETE,
        re.compile(r'.*/rest/users')
    )

    client.users.delete(1)
