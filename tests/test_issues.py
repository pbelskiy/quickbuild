import re

import responses

ISSUES_LIST_XML = r"""
<report name="issues" version="0.0" locale="en_US">
  <row ID="15" issueKey="TST-23" buildId="321" issueType="New Feature" summary="2-phase load components"
       status="Resolved" priority="Major" created="2011-06-03T14:58:47.445+08:00" updated="2011-06-03T15:27:39.418+08:00"
       resolution="Fixed" assignee="admin" reporter="admin" modifications="3">
    <changeIds>
      913fcbcdbe8f80d6c1fe5fce3bb49e1f0040a943,f090cd04725c5551f8a439fe0a53591193ea79c3
    </changeIds>
    <repositories>hg,hg</repositories>
  </row>
  <row ID="16" issueKey="TST-24" buildId="322" issueType="New Feature 2" summary="2-phase load components"
       status="Resolved" priority="Major" created="2021-06-03T14:58:47.445+08:00" updated="2021-06-03T15:27:39.418+08:00"
       resolution="Fixed" assignee="admin" reporter="admin" modifications="3">
    <changeIds>
      bb49e1f0040a943913fcbcdbe8f80d6c1fe5fce3,04725c5551f8af090cd439fe0a53591193ea79c3
    </changeIds>
    <repositories>hg,hg</repositories>
  </row>
</report>
"""

BUILDS_LIST_XML = r"""
<list>
  <build>
    <id>321</id>
    <version>1.0.15</version>
    <status>SUCCESSFUL</status>
    <beginDate>2011-06-10T17:11:35.662+08:00</beginDate>
    <duration>3409</duration>
    <scheduled>false</scheduled>
    <requester>Administrator</requester>
    <deleted>false</deleted>
  </build>
</list>
"""

CHANGES_LIST_XML = r"""
<list>
  <changeset>
    <user>steve</user>
    <date>2011-05-31T03:45:55.000+08:00</date>
    <id>f090cd04725c5551f8a439fe0a53591193ea79c3</id>
    <repositoryName>hg</repositoryName>
    <repositoryType>Mercurial</repositoryType>
    <additional>13</additional>
    <buildId>321</buildId>
    <comment>
       add a big file to related to issue TST-23, TST-24 TST-25
    </comment>
    <modifications>
      <modification>
        <action>ADD</action>
        <path>big.java</path>
        <edition>f090cd04725c5551f8a439fe0a53591193ea79c3</edition>
        <previousEdition>c11a08aa7525a01e35239b8b6f34d4f8f3bf770b</previousEdition>
        <additional>13</additional>
      </modification>
    </modifications>
  </changeset>
</list>
"""


@responses.activate
def test_get_version(client):
    responses.add(
        responses.GET,
        re.compile(r'.*/rest/jira/version'),
        content_type='text/plain',
        body='3.1',
    )

    version = client.issues.get_tracker('jira').get_version()
    assert version == '3.1'


@responses.activate
def test_get_size(client):
    responses.add(
        responses.GET,
        re.compile(r'.*/rest/jira/size/.*'),
        content_type='text/plain',
        body='29',
    )

    size = client.issues.get_tracker('jira').get_size(
        'root/My/DEV',
        from_build=100,
        to_build=150,
    )

    assert size == 29


@responses.activate
def test_get_issues(client):
    responses.add(
        responses.GET,
        re.compile(r'.*/rest/jira/issues/.*'),
        content_type='text/xml',
        body=ISSUES_LIST_XML,
    )

    issues = client.issues.get_tracker('jira').get_issues(
        19,
        build=100,
    )

    assert len(issues) == 2
    assert issues[0]['assignee'] == 'admin'


@responses.activate
def test_get_builds(client):
    responses.add(
        responses.GET,
        re.compile(r'.*/rest/jira/.+/builds/.+'),
        content_type='text/xml',
        body=BUILDS_LIST_XML,
    )

    builds = client.issues.get_tracker('jira').get_builds(5, 'QB-123')

    assert len(builds) == 1
    assert builds[0]['id'] == 321


@responses.activate
def test_get_changes(client):
    responses.add(
        responses.GET,
        re.compile(r'.*/rest/jira/.+/changes/.+'),
        content_type='text/xml',
        body=CHANGES_LIST_XML,
    )

    builds = client.issues.get_tracker('jira').get_changes(5, 'QB-123')

    assert len(builds) == 1
    assert builds[0]['user'] == 'steve'
