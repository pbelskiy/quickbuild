import re

import pytest
import responses

from quickbuild import QBError

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

DASHBOARD_INFO_XML = r"""<?xml version="1.0" encoding="UTF-8"?>

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
        <com.pmease.quickbuild.plugin.report.changes.gadget.CommitStatsGadget revision="0.0.0.0.0.0">
          <title>Commits</title>
          <configurationPath>root</configurationPath>
          <reportsets/>
          <indicators>
            <string>Commits</string>
            <string>Modifications</string>
          </indicators>
          <groupBy>BY_DAY</groupBy>
          <excludingFailed>false</excludingFailed>
          <ignoreNoBuildDays>false</ignoreNoBuildDays>
        </com.pmease.quickbuild.plugin.report.changes.gadget.CommitStatsGadget>
      </gadgetDOMs>
    </com.pmease.quickbuild.web.page.dashboard.LayoutColumn>
  </columns>
</com.pmease.quickbuild.model.Dashboard>
"""

DASHBOARD_INFO_JSON = """{
  "id" : 1,
  "user" : 1,
  "name" : "Default",
  "description" : "System default dashboard",
  "primary" : false,
  "columns" : [ {
    "width" : 100,
    "gadgetDOMs" : [ {
      "title" : "All Configurations",
      "treeRoot" : 1,
      "displayTreeRoot" : true,
      "displaySchedule" : false,
      "displayRequestCount" : true,
      "displayHistoryCount" : true,
      "@class" : "com.pmease.quickbuild.web.gadget.ConfigurationTreeGadget"
    }, {
      "title" : "Commits",
      "configurationPath" : "root",
      "reportsets" : [ ],
      "indicators" : [ "Commits", "Modifications" ],
      "groupBy" : "BY_DAY",
      "excludingFailed" : false,
      "ignoreNoBuildDays" : false,
      "@class" : "com.pmease.quickbuild.plugin.report.changes.gadget.CommitStatsGadget"
    } ]
  } ]
}
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


@responses.activate
def test_get_info(client):
    responses.add(
        responses.GET,
        re.compile(r'.*/rest/dashboards'),
        content_type='application/xml',
        body=DASHBOARD_INFO_XML,
    )

    response = client.dashboards.get_info(1)

    assert response['@class'] == 'com.pmease.quickbuild.model.Dashboard'
    assert response['id'] == 1
    assert response['columns'][0]['gadgetDOMs'][0]['@revision'] == '0.0.1'


@responses.activate
def test_update(client):
    responses.add(
        responses.POST,
        re.compile(r'.*/rest/dashboards'),
        content_type='application/xml',
        body='10',
    )

    response = client.dashboards.update(DASHBOARD_INFO_XML)
    assert response == 10


@responses.activate
def test_create(client):
    responses.add(
        responses.POST,
        re.compile(r'.*/rest/dashboards'),
        content_type='application/xml',
        body='11',
    )

    configuration_without_id = DASHBOARD_INFO_XML.replace('<id>1</id>', '')
    response = client.dashboards.create(configuration_without_id)
    assert response == 11

    with pytest.raises(QBError):
        client.dashboards.create(DASHBOARD_INFO_XML)

    with pytest.raises(QBError):
        client.dashboards.create(DASHBOARD_INFO_JSON)


@responses.activate
def test_delete(client):
    responses.add(
        responses.DELETE,
        re.compile(r'.*/rest/dashboards'),
        body='12',
    )

    response = client.dashboards.delete(12)
    assert response == 12
