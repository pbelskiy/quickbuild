import re

import pytest
import responses

from quickbuild import QBError

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

USER_INFO_XML = r"""<?xml version="1.0" encoding="UTF-8"?>

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

    xml_with_id = USER_INFO_XML
    xml_without_id = xml_with_id.replace('<id>1</id>', '')

    with pytest.raises(QBError):
        client.users.create(xml_with_id)

    response = client.users.create(xml_without_id)
    assert response == 1


@responses.activate
def test_delete(client):
    responses.add(
        responses.DELETE,
        re.compile(r'.*/rest/users')
    )

    client.users.delete(1)
