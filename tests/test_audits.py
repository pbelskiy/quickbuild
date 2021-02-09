import re

import responses

from quickbuild import QBClient


AUDITS_XML = r"""<?xml version="1.0" encoding="UTF-8"?>

<list>
  <com.pmease.quickbuild.model.Audit>
    <id>11</id>
    <user>admin</user>
    <timestamp>2021-02-03T12:18:45.168Z</timestamp>
    <source>root/</source>
    <action>Build 1.0.0 (#1) was modified via REST.</action>
    <content>&lt;?xml version="1.0" encoding="UTF-8"?&gt;

&lt;com.pmease.quickbuild.model.Build revision="0.0"&gt;
  &lt;id&gt;1&lt;/id&gt;
  &lt;configuration&gt;1&lt;/configuration&gt;
  &lt;version&gt;1.0.0&lt;/version&gt;
  &lt;requester&gt;1&lt;/requester&gt;
  &lt;scheduled&gt;false&lt;/scheduled&gt;
  &lt;status&gt;SUCCESSFUL&lt;/status&gt;
  &lt;statusDate&gt;2021-01-06T19:59:52.752Z&lt;/statusDate&gt;
  &lt;beginDate&gt;2021-01-06T19:59:52.617Z&lt;/beginDate&gt;
  &lt;duration&gt;777&lt;/duration&gt;
  &lt;waitDuration&gt;96&lt;/waitDuration&gt;
  &lt;stepRuntimes&gt;
    &lt;entry&gt;
      &lt;string&gt;master&lt;/string&gt;
      &lt;com.pmease.quickbuild.stepsupport.StepRuntime&gt;
        &lt;status&gt;SUCCESSFUL&lt;/status&gt;
        &lt;nodeAddress&gt;5d94ceab5742:8810&lt;/nodeAddress&gt;
        &lt;resources/&gt;
        &lt;waitDuration&gt;96&lt;/waitDuration&gt;
        &lt;duration&gt;11&lt;/duration&gt;
      &lt;/com.pmease.quickbuild.stepsupport.StepRuntime&gt;
    &lt;/entry&gt;
  &lt;/stepRuntimes&gt;
  &lt;repositoryRuntimes/&gt;
  &lt;secretAwareVariableValues/&gt;
&lt;/com.pmease.quickbuild.model.Build&gt;
</content>
    <previousContent>&lt;?xml version="1.0" encoding="UTF-8"?&gt;

&lt;com.pmease.quickbuild.model.Build revision="0.0"&gt;
  &lt;id&gt;1&lt;/id&gt;
  &lt;configuration&gt;1&lt;/configuration&gt;
  &lt;version&gt;1.0.0&lt;/version&gt;
  &lt;requester&gt;1&lt;/requester&gt;
  &lt;scheduled&gt;false&lt;/scheduled&gt;
  &lt;status&gt;SUCCESSFUL&lt;/status&gt;
  &lt;statusDate&gt;2021-01-06T19:59:52.752Z&lt;/statusDate&gt;
  &lt;beginDate&gt;2021-01-06T19:59:52.617Z&lt;/beginDate&gt;
  &lt;duration&gt;666&lt;/duration&gt;
  &lt;waitDuration&gt;96&lt;/waitDuration&gt;
  &lt;stepRuntimes&gt;
    &lt;entry&gt;
      &lt;string&gt;master&lt;/string&gt;
      &lt;com.pmease.quickbuild.stepsupport.StepRuntime&gt;
        &lt;status&gt;SUCCESSFUL&lt;/status&gt;
        &lt;nodeAddress&gt;5d94ceab5742:8810&lt;/nodeAddress&gt;
        &lt;resources/&gt;
        &lt;waitDuration&gt;96&lt;/waitDuration&gt;
        &lt;duration&gt;11&lt;/duration&gt;
      &lt;/com.pmease.quickbuild.stepsupport.StepRuntime&gt;
    &lt;/entry&gt;
  &lt;/stepRuntimes&gt;
  &lt;repositoryRuntimes/&gt;
  &lt;secretAwareVariableValues/&gt;
&lt;/com.pmease.quickbuild.model.Build&gt;
</previousContent>
  </com.pmease.quickbuild.model.Audit>
</list>
"""


@responses.activate
def test_get():
    responses.add(
        responses.GET,
        re.compile(r'.*/rest/audits'),
        content_type='application/xml',
        body=AUDITS_XML,
    )

    response = QBClient('http://server').audits.get(count=1)
    assert len(response) == 1
    assert response[0]['id'] == '11'


@responses.activate
def test_count():
    responses.add(
        responses.GET,
        re.compile(r'.*/rest/audits/count'),
        body='11',
    )

    response = QBClient('http://server').audits.count()
    assert response == 11
