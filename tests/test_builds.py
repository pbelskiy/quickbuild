import re

from http import HTTPStatus

import pytest
import responses

from quickbuild import AsyncQBClient, QBClient, QBNotFoundError, QBProcessingError

BUILD_INFO_XML = r"""<?xml version="1.0" encoding="UTF-8"?>

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


BUILD_SEARCH_XML = r"""<?xml version="1.0" encoding="UTF-8"?>

<list>
  <com.pmease.quickbuild.model.Build>
    <id>4</id>
    <configuration>1</configuration>
    <version>1.0.3</version>
    <requester>1</requester>
    <scheduled>false</scheduled>
    <status>SUCCESSFUL</status>
    <statusDate>2021-01-18T13:29:15.341Z</statusDate>
    <beginDate>2021-01-18T13:28:15.033Z</beginDate>
    <duration>60309</duration>
    <waitDuration>26</waitDuration>
    <stepRuntimes>
      <entry>
        <string>master</string>
        <com.pmease.quickbuild.stepsupport.StepRuntime>
          <status>SUCCESSFUL</status>
          <nodeAddress>5d94ceab5742:8810</nodeAddress>
          <resources/>
          <waitDuration>26</waitDuration>
          <duration>60192</duration>
        </com.pmease.quickbuild.stepsupport.StepRuntime>
      </entry>
      <entry>
        <string>master&gt;sleep</string>
        <com.pmease.quickbuild.stepsupport.StepRuntime>
          <status>SUCCESSFUL</status>
          <nodeAddress>5d94ceab5742:8810</nodeAddress>
          <resources/>
          <waitDuration>14</waitDuration>
          <duration>60007</duration>
        </com.pmease.quickbuild.stepsupport.StepRuntime>
      </entry>
    </stepRuntimes>
    <repositoryRuntimes/>
    <secretAwareVariableValues/>
  </com.pmease.quickbuild.model.Build>
  <com.pmease.quickbuild.model.Build>
    <id>3</id>
    <configuration>1</configuration>
    <version>1.0.2</version>
    <requester>1</requester>
    <scheduled>false</scheduled>
    <status>SUCCESSFUL</status>
    <statusDate>2021-01-17T15:49:11.770Z</statusDate>
    <beginDate>2021-01-17T15:48:11.362Z</beginDate>
    <duration>60409</duration>
    <waitDuration>32</waitDuration>
    <stepRuntimes>
      <entry>
        <string>master</string>
        <com.pmease.quickbuild.stepsupport.StepRuntime>
          <status>SUCCESSFUL</status>
          <nodeAddress>5d94ceab5742:8810</nodeAddress>
          <resources/>
          <waitDuration>32</waitDuration>
          <duration>60252</duration>
        </com.pmease.quickbuild.stepsupport.StepRuntime>
      </entry>
      <entry>
        <string>master&gt;sleep</string>
        <com.pmease.quickbuild.stepsupport.StepRuntime>
          <status>SUCCESSFUL</status>
          <nodeAddress>5d94ceab5742:8810</nodeAddress>
          <resources/>
          <waitDuration>16</waitDuration>
          <duration>60043</duration>
        </com.pmease.quickbuild.stepsupport.StepRuntime>
      </entry>
    </stepRuntimes>
    <repositoryRuntimes/>
    <secretAwareVariableValues/>
  </com.pmease.quickbuild.model.Build>
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
    assert response['id'] == '1'

    response = QBClient('http://server').builds.get_info(1, as_xml=True)
    assert isinstance(response, str)


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


@responses.activate
def test_get_dependencies():
    RESPONSE_DATA = r"""
    <?xml version="1.0" encoding="UTF-8"?>

    <list/>
    """

    responses.add(
        responses.GET,
        re.compile(r'.*/rest/builds/\d+/dependencies'),
        content_type='application/xml',
        body=RESPONSE_DATA,
    )

    response = QBClient('http://server').builds.get_dependencies(1)
    assert 'list' in response


@responses.activate
def test_get_dependents():
    RESPONSE_DATA = r"""
    <?xml version="1.0" encoding="UTF-8"?>

    <list/>
    """

    responses.add(
        responses.GET,
        re.compile(r'.*/rest/builds/\d+/dependents'),
        content_type='application/xml',
        body=RESPONSE_DATA,
    )

    response = QBClient('http://server').builds.get_dependents(1)
    assert 'list' in response


@responses.activate
def test_search():
    responses.add(
        responses.GET,
        re.compile(r'.*/rest/builds.*'),
        content_type='application/xml',
        body=BUILD_SEARCH_XML,
    )

    response = QBClient('http://server').builds.search(
        count=2,
        configuration_id=1,
        from_date='2021-01-14',
        first=3,
    )

    len(response) == 2


@responses.activate
def test_count():
    responses.add(
        responses.GET,
        re.compile(r'.*/rest/builds/count'),
        content_type='text/plain',
        body='5',
    )

    response = QBClient('http://server').builds.count(
        configuration_id=1,
        recursive=False,
        from_date='2021-01-20',
        to_date='2021-01-22',
        version='*',
        status='SUCCESSFUL',
        user_id=2,
        promoted_from_id=1,
    )

    assert response == 5


@responses.activate
def test_update():
    responses.add(
        responses.POST,
        re.compile(r'.*/rest/builds'),
        content_type='text/plain',
        body='5',
    )

    response = QBClient('http://server').builds.update(BUILD_INFO_XML)
    assert response == 5


@responses.activate
def test_create():
    responses.add(
        responses.POST,
        re.compile(r'.*/rest/builds'),
        content_type='text/plain',
        body='5',
    )

    response = QBClient('http://server').builds.create(BUILD_INFO_XML)
    assert response == 5


@responses.activate
def test_delete():
    responses.add(
        responses.DELETE,
        re.compile(r'.*/rest/builds'),
        content_type='text/plain',
    )

    QBClient('http://server').builds.delete(5)
