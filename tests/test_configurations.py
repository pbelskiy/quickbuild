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

GET_CONFIGURATION_INFO_XML = r"""<?xml version="1.0" encoding="UTF-8"?>

<com.pmease.quickbuild.model.Configuration>
  <id>1</id>
  <concurrent>false</concurrent>
  <triggerDependents>false</triggerDependents>
  <recordSCMChanges>true</recordSCMChanges>
  <pauseNotification>false</pauseNotification>
  <queueChangedBranchesOnly>false</queueChangedBranchesOnly>
  <auditBuildRequest>true</auditBuildRequest>
  <disabled>false</disabled>
  <showConfigurationInPipeline>true</showConfigurationInPipeline>
  <legacyCmdMode>false</legacyCmdMode>
  <name>root</name>
  <order>100</order>
  <snapshotTaking class="com.pmease.quickbuild.setting.configuration.snapshot.TakeReferencedSnapshots"/>
  <buildCondition class="com.pmease.quickbuild.setting.configuration.buildcondition.AlwaysBuild"/>
  <showParallelStepsVertically>false</showParallelStepsVertically>
  <versionManagerDOM>
    <com.pmease.quickbuild.setting.configuration.version.UseSpecifiedVersion revision="0.0.0">
      <version>1.0.12</version>
    </com.pmease.quickbuild.setting.configuration.version.UseSpecifiedVersion>
  </versionManagerDOM>
  <storageSetting class="com.pmease.quickbuild.setting.configuration.storage.UseGlobalStorage"/>
  <workspaceSetting class="com.pmease.quickbuild.setting.configuration.workspace.UseNameAsWorkspace">
    <removeWorkspaceUponDeletion>true</removeWorkspaceUponDeletion>
  </workspaceSetting>
  <artifactStorageDOM>
    <com.pmease.quickbuild.setting.configuration.artifactstorage.ServerArtifactStorage revision="0.0.0"/>
  </artifactStorageDOM>
  <schedule class="com.pmease.quickbuild.taskschedule.schedule.NoSchedule">
    <paused>false</paused>
    <randomRange>60</randomRange>
  </schedule>
  <buildCleanupStrategy class="com.pmease.quickbuild.setting.configuration.buildcleanup.DisableAutoCleanupBuild"/>
  <artifactCleanupStrategy class="com.pmease.quickbuild.setting.configuration.artifactcleanup.DisableAutoCleanupArtifact">
    <cleanupBuildLog>false</cleanupBuildLog>
  </artifactCleanupStrategy>
  <priority>5</priority>
  <timeout>720</timeout>
  <forceKillTimeout>5</forceKillTimeout>
  <logLevel class="com.pmease.quickbuild.setting.configuration.loglevel.InfoLogLevel"/>
  <statusDate>2021-03-27T15:56:14.340Z</statusDate>
  <pluginSettingDOMs/>
  <data/>
  <stepDOMs>
    <entry>
      <string>master</string>
      <com.pmease.quickbuild.stepsupport.SequentialStep revision="0.15.2.2">
        <name>master</name>
        <inheritable>true</inheritable>
        <enabled>true</enabled>
        <executeCondition class="com.pmease.quickbuild.setting.step.executecondition.AllPreviousSiblingStepsSuccessful"/>
        <nodeMatcher class="com.pmease.quickbuild.setting.step.nodematcher.ParentNodeMatcher"/>
        <nodePreference class="com.pmease.quickbuild.setting.step.nodepreference.PreferLeastLoadedNode"/>
        <timeout>0</timeout>
        <disconnectTolerance>0</disconnectTolerance>
        <showLinksInLog>false</showLinksInLog>
        <preExecuteAction class="com.pmease.quickbuild.setting.step.executeaction.NoAction"/>
        <postExecuteAction class="com.pmease.quickbuild.setting.step.executeaction.NoAction"/>
        <repetitions/>
        <childStepNames>
          <string>sleep</string>
        </childStepNames>
        <successCondition class="com.pmease.quickbuild.setting.step.successcondition.AllChildStepsSuccessful"/>
        <environments/>
      </com.pmease.quickbuild.stepsupport.SequentialStep>
    </entry>
    <entry>
      <string>sleep</string>
      <com.pmease.quickbuild.plugin.basis.CommandBuildStep revision="0.15.4">
        <name>sleep</name>
        <inheritable>true</inheritable>
        <enabled>true</enabled>
        <executeCondition class="com.pmease.quickbuild.setting.step.executecondition.AllPreviousSiblingStepsSuccessful"/>
        <nodeMatcher class="com.pmease.quickbuild.setting.step.nodematcher.ParentNodeMatcher"/>
        <nodePreference class="com.pmease.quickbuild.setting.step.nodepreference.PreferLeastLoadedNode"/>
        <timeout>0</timeout>
        <disconnectTolerance>0</disconnectTolerance>
        <showLinksInLog>false</showLinksInLog>
        <preExecuteAction class="com.pmease.quickbuild.setting.step.executeaction.NoAction"/>
        <postExecuteAction class="com.pmease.quickbuild.setting.step.executeaction.NoAction"/>
        <repetitions/>
        <command>sleep 100</command>
        <environments/>
        <waitForFinish>true</waitForFinish>
        <returnCode>0</returnCode>
      </com.pmease.quickbuild.plugin.basis.CommandBuildStep>
    </entry>
  </stepDOMs>
  <repositoryDOMs/>
  <aggregationDOMs/>
  <variables/>
  <notifications/>
  <promotions/>
</com.pmease.quickbuild.model.Configuration>
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


@responses.activate
def test_get_info():
    responses.add(
        responses.GET,
        re.compile(r'.*/rest/configurations/1'),
        content_type='application/xml',
        body=GET_CONFIGURATION_INFO_XML,
    )

    response = QBClient('http://server').configurations.get_info(1)
    assert response['name'] == 'root'


@responses.activate
def test_get_path():
    responses.add(
        responses.GET,
        re.compile(r'.*/rest/configurations/1/path'),
        body='root',
    )

    response = QBClient('http://server').configurations.get_path(1)
    assert response == 'root'
