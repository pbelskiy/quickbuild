import json

from quickbuild.helpers import ContentType, response2py

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
</list>
"""

DASHBOARDS_JSON = """[ {
  "@class" : "com.pmease.quickbuild.model.Dashboard",
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
} ]
"""


def test_xml_json_equal():
    parsed_xml = response2py(DASHBOARDS_XML, content_type=ContentType.PARSE)
    parsed_json = json.loads(DASHBOARDS_JSON)
    assert len(parsed_xml) == len(parsed_json)

    data_xml = parsed_xml[0]
    data_json = parsed_json[0]

    assert data_xml['@class'] == data_json['@class']
    assert data_xml['id'] == data_json['id']
    assert data_xml['user'] == data_json['user']
    assert data_xml['name'] == data_json['name']
    assert data_xml['description'] == data_json['description']
    assert data_xml['primary'] is data_json['primary']

    assert len(data_xml['columns']) == len(data_json['columns'])
    assert isinstance(data_xml['columns'], list)
    assert isinstance(data_json['columns'], list)

    column_xml = data_xml['columns'][0]
    column_json = data_json['columns'][0]

    assert column_xml['width'] == column_json['width']
    assert len(column_xml['gadgetDOMs']) == len(column_json['gadgetDOMs'])
    assert column_xml['gadgetDOMs'][0]['@class'] == column_json['gadgetDOMs'][0]['@class']
