import re

import responses

from quickbuild import QBClient

GET_CONFIGURATIONS_XML = r"""<?xml version="1.0" encoding="UTF-8"?>

<list>
  <com.pmease.quickbuild.model.Configuration>
    <id>1</id>
    <disabled>false</disabled>
    <name>root</name>
    <order>100</order>
    <schedule class="com.pmease.quickbuild.taskschedule.schedule.NoSchedule">
      <paused>false</paused>
      <randomRange>60</randomRange>
    </schedule>
    <statusDate>2021-03-27T15:56:14.340Z</statusDate>
    <pluginSettingDOMs/>
    <data/>
    <stepDOMs/>
    <repositoryDOMs/>
    <aggregationDOMs/>
    <variables/>
    <notifications/>
    <promotions/>
  </com.pmease.quickbuild.model.Configuration>
  <com.pmease.quickbuild.model.Configuration>
    <id>2</id>
    <disabled>true</disabled>
    <parent>1</parent>
    <name>~maintenance</name>
    <order>100</order>
    <statusDate>2021-03-08T16:51:42.206Z</statusDate>
    <pluginSettingDOMs/>
    <data/>
    <stepDOMs/>
    <repositoryDOMs/>
    <aggregationDOMs/>
    <variables/>
    <notifications/>
    <promotions/>
  </com.pmease.quickbuild.model.Configuration>
  <com.pmease.quickbuild.model.Configuration>
    <id>3</id>
    <disabled>false</disabled>
    <parent>2</parent>
    <name>sync configurations</name>
    <description>Test</description>
    <order>100</order>
    <statusDate>2021-03-08T16:51:42.216Z</statusDate>
    <pluginSettingDOMs/>
    <data/>
    <stepDOMs/>
    <repositoryDOMs/>
    <aggregationDOMs/>
    <variables/>
    <notifications/>
    <promotions/>
  </com.pmease.quickbuild.model.Configuration>
</list>
"""

GET_CHILD_CONFIGURATIONS_XML = r"""<?xml version="1.0" encoding="UTF-8"?>

<list>
  <com.pmease.quickbuild.model.Configuration>
    <id>2</id>
    <disabled>true</disabled>
    <parent>1</parent>
    <name>~maintenance</name>
    <order>100</order>
    <statusDate>2021-03-08T16:51:42.206Z</statusDate>
    <pluginSettingDOMs/>
    <data/>
    <stepDOMs/>
    <repositoryDOMs/>
    <aggregationDOMs/>
    <variables/>
    <notifications/>
    <promotions/>
  </com.pmease.quickbuild.model.Configuration>
</list>
"""

GET_DESCENDENT_CONFIGURATIONS_XML = r"""<?xml version="1.0" encoding="UTF-8"?>

<list>
  <com.pmease.quickbuild.model.Configuration>
    <id>2</id>
    <disabled>true</disabled>
    <parent>1</parent>
    <name>~maintenance</name>
    <order>100</order>
    <statusDate>2021-03-08T16:51:42.206Z</statusDate>
    <pluginSettingDOMs/>
    <data/>
    <stepDOMs/>
    <repositoryDOMs/>
    <aggregationDOMs/>
    <variables/>
    <notifications/>
    <promotions/>
  </com.pmease.quickbuild.model.Configuration>
  <com.pmease.quickbuild.model.Configuration>
    <id>3</id>
    <disabled>false</disabled>
    <parent>2</parent>
    <name>sync configurations</name>
    <description>This configuration is created to demonstrate how to use the "Maintenance/Sync Configurations" step to sync configuration settings from remote QuickBuild server. To sync, just run this configuration and fill in necessary information on the build option page.</description>
    <order>100</order>
    <statusDate>2021-03-08T16:51:42.216Z</statusDate>
    <pluginSettingDOMs/>
    <data/>
    <stepDOMs/>
    <repositoryDOMs/>
    <aggregationDOMs/>
    <variables/>
    <notifications/>
    <promotions/>
  </com.pmease.quickbuild.model.Configuration>
</list>
"""


@responses.activate
def test_get():
    responses.add(
        responses.GET,
        re.compile(r'.*/rest/configurations'),
        content_type='application/xml',
        body=GET_CONFIGURATIONS_XML,
    )

    response = QBClient('http://server').configurations.get()
    assert len(response) == 3
    assert response[0]['name'] == 'root'


@responses.activate
def test_get_child():
    responses.add(
        responses.GET,
        re.compile(r'.*/rest/configurations'),
        content_type='application/xml',
        body=GET_CHILD_CONFIGURATIONS_XML,
    )

    response = QBClient('http://server').configurations.get_child(1)
    assert len(response) == 1
    assert response[0]['id'] == '2'


@responses.activate
def test_get_descendent():
    responses.add(
        responses.GET,
        re.compile(r'.*/rest/configurations'),
        content_type='application/xml',
        body=GET_DESCENDENT_CONFIGURATIONS_XML,
    )

    response = QBClient('http://server').configurations.get_descendent(1)
    assert len(response) == 2
    assert response[0]['id'] == '2'
