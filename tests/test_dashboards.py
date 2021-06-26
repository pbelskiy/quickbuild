import re

import responses

DASHBOARDS_XML = r"""<?xml version="1.0" encoding="UTF-8"?>

<list>
  <com.pmease.quickbuild.model.Dashboard>
    <id>1</id>
    <user>1</user>
    <name>Default</name>
    <description>System default dashboard</description>
    <primary>false</primary>
    <columns>
      <com.pmease.quickbuild.web.page.dashboard.LayoutColumn>
        <width>100</width>
        <gadgetDOMs>
          <com.pmease.quickbuild.web.gadget.ConfigurationTreeGadget revision="0.0.1">
            <title>All Configurations</title>
            <treeRoot>1</treeRoot>
            <displayTreeRoot>true</displayTreeRoot>
            <displaySchedule>false</displaySchedule>
            <displayRequestCount>true</displayRequestCount>
            <displayHistoryCount>true</displayHistoryCount>
          </com.pmease.quickbuild.web.gadget.ConfigurationTreeGadget>
        </gadgetDOMs>
      </com.pmease.quickbuild.web.page.dashboard.LayoutColumn>
    </columns>
  </com.pmease.quickbuild.model.Dashboard>
</list>
"""


@responses.activate
def test_get(client):
    responses.add(
        responses.GET,
        re.compile(r'.*/rest/dashboards'),
        content_type='application/xml',
        body=DASHBOARDS_XML,
    )

    response = client.dashboards.get()
    assert len(response) == 1
    assert response[0]['id'] == 1
    assert response[0]['user'] == 1
    assert response[0]['name'] == 'Default'
    assert response[0]['primary'] is False
    assert response[0]['columns'][0]['width'] == 100
