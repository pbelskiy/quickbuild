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
