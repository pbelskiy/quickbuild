import re

import responses

from quickbuild import QBClient


@responses.activate
def test_get_info():
    RESPONSE_DATA = r"""
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

    responses.add(
        responses.GET,
        re.compile(r'.*/rest/builds/\d+'),
        content_type='application/xml',
        body=RESPONSE_DATA,
    )

    client = QBClient('http://server', 'login', 'password')

    response = client.builds.get_info(1)

    assert '<id>1</id>' in response


@responses.activate
def test_get_status():
    RESPONSE_DATA = 'SUCCESS'

    responses.add(
        responses.GET,
        re.compile(r'.*/rest/builds/\d+/status'),
        body=RESPONSE_DATA,
    )

    client = QBClient('http://server', 'login', 'password')

    response = client.builds.get_status(1)

    assert response == RESPONSE_DATA
