import re

import responses

ISSUES_LIST_XML = r"""
<report name="issues" version="0.0" locale="en_US">
  <row ID="15" issueKey="TST-23" buildId="321" issueType="New Feature" summary="2-phase load components" status="Resolved" priority="Major" created="2011-06-03T14:58:47.445+08:00" updated="2011-06-03T15:27:39.418+08:00" resolution="Fixed" assignee="admin" reporter="admin" modifications="3">
    <changeIds>
      913fcbcdbe8f80d6c1fe5fce3bb49e1f0040a943,f090cd04725c5551f8a439fe0a53591193ea79c3
    </changeIds>
    <repositories>hg,hg</repositories>
  </row>
  <row ID="16" issueKey="TST-24" buildId="322" issueType="New Feature 2" summary="2-phase load components" status="Resolved" priority="Major" created="2021-06-03T14:58:47.445+08:00" updated="2021-06-03T15:27:39.418+08:00" resolution="Fixed" assignee="admin" reporter="admin" modifications="3">
    <changeIds>
      bb49e1f0040a943913fcbcdbe8f80d6c1fe5fce3,04725c5551f8af090cd439fe0a53591193ea79c3
    </changeIds>
    <repositories>hg,hg</repositories>
  </row>
</report>
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
