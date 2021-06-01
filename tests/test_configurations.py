import datetime
import re

import responses


CONFIGURATIONS_XML = r"""<?xml version="1.0" encoding="UTF-8"?>

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

CHILD_CONFIGURATIONS_XML = r"""<?xml version="1.0" encoding="UTF-8"?>

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

DESCENDENT_CONFIGURATIONS_XML = r"""<?xml version="1.0" encoding="UTF-8"?>

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

CONFIGURATION_INFO_XML = r"""<?xml version="1.0" encoding="UTF-8"?>

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
def test_get(client):
    responses.add(
        responses.GET,
        re.compile(r'.*/rest/configurations'),
        content_type='application/xml',
        body=CONFIGURATIONS_XML,
    )

    response = client.configurations.get()
    assert len(response) == 3
    assert response[0]['name'] == 'root'


@responses.activate
def test_get_child(client):
    responses.add(
        responses.GET,
        re.compile(r'.*/rest/configurations'),
        content_type='application/xml',
        body=CHILD_CONFIGURATIONS_XML,
    )

    response = client.configurations.get_child(1)
    assert len(response) == 1
    assert response[0]['id'] == 2


@responses.activate
def test_get_descendent(client):
    responses.add(
        responses.GET,
        re.compile(r'.*/rest/configurations'),
        content_type='application/xml',
        body=DESCENDENT_CONFIGURATIONS_XML,
    )

    response = client.configurations.get_descendent(1)
    assert len(response) == 2
    assert response[0]['id'] == 2


@responses.activate
def test_get_info_as_json(client):
    responses.add(
        responses.GET,
        re.compile(r'.*/rest/configurations/1'),
        content_type='application/xml',
        body=CONFIGURATION_INFO_XML,
    )

    response = client.configurations.get_info(1)
    assert response['name'] == 'root'
    assert response['id'] == 1
    assert response['concurrent'] is False
    assert response['schedule']['paused'] is False


@responses.activate
def test_get_info_as_xml(client):
    responses.add(
        responses.GET,
        re.compile(r'.*/rest/configurations/1'),
        content_type='application/xml',
        body=CONFIGURATION_INFO_XML,
    )

    response = client.configurations.get_info(1, as_xml=True)
    assert isinstance(response, str)


@responses.activate
def test_get_path(client):
    responses.add(
        responses.GET,
        re.compile(r'.*/rest/configurations/1/path'),
        body='root',
    )

    response = client.configurations.get_path(1)
    assert response == 'root'


@responses.activate
def test_get_name(client):
    responses.add(
        responses.GET,
        re.compile(r'.*/rest/configurations/1/name'),
        body='root',
    )

    response = client.configurations.get_name(1)
    assert response == 'root'


@responses.activate
def test_get_description(client):
    responses.add(
        responses.GET,
        re.compile(r'.*/rest/configurations/1/description'),
        body='root',
    )

    response = client.configurations.get_description(1)
    assert response == 'root'


@responses.activate
def test_get_error_message(client):
    responses.add(
        responses.GET,
        re.compile(r'.*/rest/configurations/1/error_message'),
        body='error_message',
    )

    response = client.configurations.get_error_message(1)
    assert response == 'error_message'


@responses.activate
def test_get_run_mode(client):
    responses.add(
        responses.GET,
        re.compile(r'.*/rest/configurations/1/run_mode'),
        body='run_mode',
    )

    response = client.configurations.get_run_mode(1)
    assert response == 'run_mode'


@responses.activate
def test_get_schedule_empty(client):
    CONFIGURATION_SCHEDULE_EMPTY_XML = r"""<?xml version="1.0" encoding="UTF-8"?>

    <com.pmease.quickbuild.taskschedule.schedule.NoSchedule>
      <paused>false</paused>
      <randomRange>60</randomRange>
    </com.pmease.quickbuild.taskschedule.schedule.NoSchedule>
    """
    responses.add(
        responses.GET,
        re.compile(r'.*/rest/configurations/1/schedule'),
        content_type='application/xml',
        body=CONFIGURATION_SCHEDULE_EMPTY_XML,
    )

    response = client.configurations.get_schedule(1)
    assert response['paused'] is False


@responses.activate
def test_get_schedule_periodical(client):
    CONFIGURATION_SCHEDULE_PERIODICAL_XML = r"""<?xml version="1.0" encoding="UTF-8"?>

    <com.pmease.quickbuild.taskschedule.schedule.PeriodicalSchedule>
      <paused>true</paused>
      <randomRange>60</randomRange>
      <repeatInterval>300</repeatInterval>
    </com.pmease.quickbuild.taskschedule.schedule.PeriodicalSchedule>
    """

    responses.add(
        responses.GET,
        re.compile(r'.*/rest/configurations/1/schedule'),
        content_type='application/xml',
        body=CONFIGURATION_SCHEDULE_PERIODICAL_XML,
    )

    response = client.configurations.get_schedule(1)
    assert response['repeatInterval'] == 300


@responses.activate
def test_get_schedule_cron_xml(client):
    CONFIGURATION_SCHEDULE_CRON_XML = r"""<?xml version="1.0" encoding="UTF-8"?>

    <com.pmease.quickbuild.taskschedule.schedule.CronSchedule>
      <paused>false</paused>
      <randomRange>120</randomRange>
      <expression>0 0 1 * * ?</expression>
    </com.pmease.quickbuild.taskschedule.schedule.CronSchedule>
    """

    responses.add(
        responses.GET,
        re.compile(r'.*/rest/configurations/1/schedule'),
        content_type='application/xml',
        body=CONFIGURATION_SCHEDULE_CRON_XML,
    )

    response = client.configurations.get_schedule(1)
    assert response['expression'] == '0 0 1 * * ?'


@responses.activate
def test_get_schedule_cron_json(client):
    CONFIGURATION_SCHEDULE_CRON_JSON = r"""{
        "paused" : false,
        "randomRange" : 120,
        "expression" : "0 0 1 * * ?"
    }
    """

    responses.add(
        responses.GET,
        re.compile(r'.*/rest/configurations/1/schedule'),
        content_type='application/json',
        body=CONFIGURATION_SCHEDULE_CRON_JSON,
    )

    response = client.configurations.get_schedule(1)
    assert response['paused'] is False
    assert response['randomRange'] == 120
    assert response['expression'] == '0 0 1 * * ?'


@responses.activate
def test_get_average_duration(client):
    responses.add(
        responses.GET,
        re.compile(r'.*/rest/configurations/1/average_duration'),
        body='71831',
    )

    response = client.configurations.get_average_duration(
        1,
        from_date=datetime.date.today(),
        to_date=datetime.date.today() - datetime.timedelta(days=10)
    )

    assert response == 71831


@responses.activate
def test_get_success_rate(client):
    responses.add(
        responses.GET,
        re.compile(r'.*/rest/configurations/1/success_rate'),
        body='42',
    )

    response = client.configurations.get_success_rate(
        1,
        from_date=datetime.date.today(),
        to_date=datetime.date.today() - datetime.timedelta(days=50)
    )

    assert response == 42


@responses.activate
def test_get_parent(client):
    responses.add(
        responses.GET,
        re.compile(r'.*/rest/configurations/1/parent'),
        body='55',
    )

    response = client.configurations.get_parent(1)
    assert response == 55


@responses.activate
def test_update(client):
    responses.add(
        responses.POST,
        re.compile(r'.*/rest/configurations'),
        body='1991',
    )

    response = client.configurations.update(CONFIGURATION_INFO_XML)
    assert response == 1991


@responses.activate
def test_create(client):
    responses.add(
        responses.POST,
        re.compile(r'.*/rest/configurations'),
        body='1991',
    )

    response = client.configurations.create(CONFIGURATION_INFO_XML)
    assert response == 1991


@responses.activate
def test_delete(client):
    responses.add(
        responses.DELETE,
        re.compile(r'.*/rest/configurations/\d'),
    )

    response = client.configurations.delete(9)
    assert response == ''
