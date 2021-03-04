import re

import responses

from quickbuild import QBClient

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
def test_get():
    responses.add(
        responses.GET,
        re.compile(r'.*/rest/groups'),
        content_type='application/xml',
        body=GROUPS_XML,
    )

    response = QBClient('http://server').groups.get()
    assert len(response) == 1
    assert response[0]['id'] == '1'


@responses.activate
def test_get_info():
    responses.add(
        responses.GET,
        re.compile(r'.*/rest/groups/1'),
        content_type='application/xml',
        body=GROUP_INFO_XML,
    )

    response = QBClient('http://server').groups.get_info(1)
    assert response['id'] == '1'


@responses.activate
def test_update():
    responses.add(
        responses.POST,
        re.compile(r'.*/rest/groups'),
        content_type='text/plain',
        body='1',
    )

    response = QBClient('http://server').groups.update(GROUP_INFO_XML)
    assert response == 1


@responses.activate
def test_create():
    responses.add(
        responses.POST,
        re.compile(r'.*/rest/groups'),
        content_type='text/plain',
        body='1',
    )

    response = QBClient('http://server').groups.create(GROUP_INFO_XML)
    assert response == 1


@responses.activate
def test_delete():
    responses.add(
        responses.DELETE,
        re.compile(r'.*/rest/groups/(\d+)'),
    )

    QBClient('http://server').groups.delete(1)
