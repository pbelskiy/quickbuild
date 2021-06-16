import re

import pytest
import responses

from quickbuild import QBError
from quickbuild.helpers import ContentType

GROUPS_XML = r"""<?xml version="1.0" encoding="UTF-8"?>

<list>
  <com.pmease.quickbuild.model.Group>
    <id>1</id>
    <name>test</name>
    <admin>false</admin>
    <restAccessAllowed>true</restAccessAllowed>
    <nodeAttributesAllowed>false</nodeAttributesAllowed>
    <systemLogAllowed>false</systemLogAllowed>
    <expandAllAllowed>false</expandAllAllowed>
    <agentAllowed>false</agentAllowed>
    <scriptAllowed>false</scriptAllowed>
    <shareDashboardAllowed>false</shareDashboardAllowed>
    <viewAlertsAllowed>false</viewAlertsAllowed>
    <forceHttps>false</forceHttps>
    <pluginSettingDOMs/>
  </com.pmease.quickbuild.model.Group>
</list>
"""

GROUP_INFO_XML = r"""<?xml version="1.0" encoding="UTF-8"?>

<com.pmease.quickbuild.model.Group>
  <id>1</id>
  <name>test</name>
  <admin>false</admin>
  <restAccessAllowed>true</restAccessAllowed>
  <nodeAttributesAllowed>false</nodeAttributesAllowed>
  <systemLogAllowed>false</systemLogAllowed>
  <expandAllAllowed>false</expandAllAllowed>
  <agentAllowed>false</agentAllowed>
  <scriptAllowed>false</scriptAllowed>
  <shareDashboardAllowed>false</shareDashboardAllowed>
  <viewAlertsAllowed>false</viewAlertsAllowed>
  <forceHttps>false</forceHttps>
  <pluginSettingDOMs/>
</com.pmease.quickbuild.model.Group>
"""


@responses.activate
def test_get(client):
    responses.add(
        responses.GET,
        re.compile(r'.*/rest/groups'),
        content_type='application/xml',
        body=GROUPS_XML,
    )

    response = client.groups.get()
    assert len(response) == 1
    assert response[0]['id'] == 1
    assert response[0]['admin'] is False


@responses.activate
def test_get_info_as_json(client):
    responses.add(
        responses.GET,
        re.compile(r'.*/rest/groups/1'),
        content_type='application/xml',
        body=GROUP_INFO_XML,
    )

    response = client.groups.get_info(1)
    assert response['id'] == 1


@responses.activate
def test_get_info_as_xml(client):
    responses.add(
        responses.GET,
        re.compile(r'.*/rest/groups/1'),
        content_type='application/xml',
        body=GROUP_INFO_XML,
    )

    response = client.groups.get_info(1, content_type=ContentType.XML)
    assert isinstance(response, str)


@responses.activate
def test_update(client):
    responses.add(
        responses.POST,
        re.compile(r'.*/rest/groups'),
        content_type='text/plain',
        body='1',
    )

    response = client.groups.update(GROUP_INFO_XML)
    assert response == 1


@responses.activate
def test_create(client):
    responses.add(
        responses.POST,
        re.compile(r'.*/rest/groups'),
        content_type='text/plain',
        body='1',
    )

    xml_with_id = GROUP_INFO_XML
    xml_without_id = xml_with_id.replace('<id>1</id>', '')

    with pytest.raises(QBError):
        client.groups.create(xml_with_id)

    response = client.groups.create(xml_without_id)
    assert response == 1


@responses.activate
def test_delete(client):
    responses.add(
        responses.DELETE,
        re.compile(r'.*/rest/groups/(\d+)'),
    )

    client.groups.delete(1)
