import re

from http import HTTPStatus

import pytest
import responses

from quickbuild import AsyncQBClient, QBClient, QBNotFoundError, QBProcessingError

BUILD_INFO_XML = r"""
<?xml version="1.0" encoding="UTF-8"?>

<com.pmease.quickbuild.model.Build>
  <id>1</id>
  <configuration>1</configuration>
  <version>1.0.0</version>
  <requester>1</requester>
  <scheduled>false</scheduled>
  <status>SUCCESSFUL</status>
  <statusDate>2021-01-06T19:59:52.752Z</statusDate>
  <beginDate>2021-01-06T19:59:52.617Z</beginDate>
  <duration>137</duration>
  <waitDuration>96</waitDuration>
  <stepRuntimes>
    <entry>
      <string>master</string>
      <com.pmease.quickbuild.stepsupport.StepRuntime>
        <status>SUCCESSFUL</status>
        <nodeAddress>5d94ceab5742:8810</nodeAddress>
        <resources/>
        <waitDuration>96</waitDuration>
        <duration>11</duration>
      </com.pmease.quickbuild.stepsupport.StepRuntime>
    </entry>
  </stepRuntimes>
  <repositoryRuntimes/>
  <secretAwareVariableValues/>
</com.pmease.quickbuild.model.Build>
"""


BUILD_STEPS_XML = r"""
<?xml version="1.0" encoding="UTF-8"?>

<list>
  <com.pmease.quickbuild.stepsupport.SequentialStep>
    <name>master</name>
    <enabled>true</enabled>
    <executeCondition class="com.pmease.quickbuild.setting.step.executecondition.AllPreviousSiblingStepsSuccessful"/>
    <nodeMatcher class="com.pmease.quickbuild.setting.step.nodematcher.ParentNodeMatcher"/>
    <nodePreference class="com.pmease.quickbuild.setting.step.nodepreference.PreferLeastLoadedNode"/>
    <timeout>0</timeout>
    <preExecuteAction class="com.pmease.quickbuild.setting.step.executeaction.NoAction"/>
    <postExecuteAction class="com.pmease.quickbuild.setting.step.executeaction.NoAction"/>
    <repetitions/>
    <path>
      <elements>
        <com.pmease.quickbuild.stepsupport.StepPath_-Element>
          <stepName>master</stepName>
          <params class="linked-hash-map"/>
        </com.pmease.quickbuild.stepsupport.StepPath_-Element>
      </elements>
    </path>
    <childStepNames>
      <string>sleep</string>
    </childStepNames>
    <successCondition class="com.pmease.quickbuild.setting.step.successcondition.AllChildStepsSuccessful"/>
    <environments/>
  </com.pmease.quickbuild.stepsupport.SequentialStep>
  <com.pmease.quickbuild.plugin.basis.CommandlineBuildStep>
    <name>sleep</name>
    <enabled>true</enabled>
    <executeCondition class="com.pmease.quickbuild.setting.step.executecondition.AllPreviousSiblingStepsSuccessful"/>
    <nodeMatcher class="com.pmease.quickbuild.setting.step.nodematcher.ParentNodeMatcher"/>
    <nodePreference class="com.pmease.quickbuild.setting.step.nodepreference.PreferLeastLoadedNode"/>
    <timeout>0</timeout>
    <preExecuteAction class="com.pmease.quickbuild.setting.step.executeaction.NoAction"/>
    <postExecuteAction class="com.pmease.quickbuild.setting.step.executeaction.NoAction"/>
    <repetitions/>
    <path>
      <elements>
        <com.pmease.quickbuild.stepsupport.StepPath_-Element>
          <stepName>master</stepName>
          <params class="linked-hash-map"/>
        </com.pmease.quickbuild.stepsupport.StepPath_-Element>
        <com.pmease.quickbuild.stepsupport.StepPath_-Element>
          <stepName>sleep</stepName>
          <params class="linked-hash-map"/>
        </com.pmease.quickbuild.stepsupport.StepPath_-Element>
      </elements>
    </path>
    <command>sleep 60</command>
    <environments/>
    <waitForFinish>true</waitForFinish>
    <returnCode>0</returnCode>
  </com.pmease.quickbuild.plugin.basis.CommandlineBuildStep>
</list>
"""


@responses.activate
def test_get_info():
    responses.add(
        responses.GET,
        re.compile(r'.*/rest/builds/\d+'),
        content_type='application/xml',
        body=BUILD_INFO_XML,
    )

    response = QBClient('http://server').builds.get_info(1)
    assert '<id>1</id>' in response


@responses.activate
def test_get_status():
    RESPONSE_DATA = 'SUCCESS'

    responses.add(
        responses.GET,
        re.compile(r'.*/rest/builds/\d+/status'),
        body=RESPONSE_DATA,
    )

    response = QBClient('http://server').builds.get_status(1)
    assert response == RESPONSE_DATA


@responses.activate
def test_get_status_not_found():
    responses.add(
        responses.GET,
        re.compile(r'.*/rest/builds/\d+/status'),
        status=HTTPStatus.NOT_FOUND
    )

    with pytest.raises(QBNotFoundError):
        QBClient('http://server').builds.get_status(2)


@responses.activate
def test_get_begin_date():
    RESPONSE_DATA = '1609963192617'  # 2021-01-06 22:59:52.617000

    responses.add(
        responses.GET,
        re.compile(r'.*/rest/builds/\d+/begin_date'),
        body=RESPONSE_DATA,
    )

    response = QBClient('http://server').builds.get_begin_date(1)
    assert response.year == 2021


@pytest.mark.asyncio
async def test_get_begin_date_async(aiohttp_mock):
    RESPONSE_DATA = '1609963192617'  # 2021-01-06 22:59:52.617000

    try:
        client = AsyncQBClient('http://server')

        aiohttp_mock.get(
            re.compile(r'.*/rest/builds/\d+/begin_date'),
            body=RESPONSE_DATA,
        )

        response = await client.builds.get_begin_date(1)
        assert response.year == 2021
    finally:
        await client.close()


@responses.activate
def test_get_version():
    RESPONSE_DATA = '1.0.0'

    responses.add(
        responses.GET,
        re.compile(r'.*/rest/builds/\d+/version'),
        body=RESPONSE_DATA,
    )

    response = QBClient('http://server').builds.get_version(1)
    assert response == RESPONSE_DATA


@responses.activate
def test_get_duration():
    RESPONSE_DATA = '137'

    responses.add(
        responses.GET,
        re.compile(r'.*/rest/builds/\d+/duration'),
        body=RESPONSE_DATA,
    )

    response = QBClient('http://server').builds.get_duration(1)
    assert response == 137


@responses.activate
def test_get_request_id():
    RESPONSE_DATA = 'fd2339a1-bc71-429d-b4ee-0ac650c342fe'

    responses.add(
        responses.GET,
        re.compile(r'.*/rest/builds/\d+/request_id'),
        body=RESPONSE_DATA,
    )

    response = QBClient('http://server').builds.get_request_id(1)
    assert response == RESPONSE_DATA


@responses.activate
def test_get_request_id_finished():
    responses.add(
        responses.GET,
        re.compile(r'.*/rest/builds/\d+/request_id'),
        status=HTTPStatus.NO_CONTENT,
    )

    with pytest.raises(QBProcessingError):
        QBClient('http://server').builds.get_request_id(1)


@responses.activate
def test_get_steps():
    responses.add(
        responses.GET,
        re.compile(r'.*/rest/builds/\d+/steps'),
        content_type='application/xml',
        body=BUILD_STEPS_XML,
    )

    response = QBClient('http://server').builds.get_steps(1)
    assert '<name>master</name>' in response


@responses.activate
def test_get_repositories():
    BUILD_REPOSITORIES_XML = r"""
    <?xml version="1.0" encoding="UTF-8"?>

    <list/>
    """

    responses.add(
        responses.GET,
        re.compile(r'.*/rest/builds/\d+/repositories'),
        content_type='application/xml',
        body=BUILD_REPOSITORIES_XML,
    )

    response = QBClient('http://server').builds.get_repositories(1)
    assert 'list' in response
