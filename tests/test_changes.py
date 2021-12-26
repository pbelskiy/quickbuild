import re

import responses

CHANGESETS_XML = r"""<list>
  <changeset>
    <user>steve</user>
    <date>2011-06-03T15:11:40.000+08:00</date>
    <id>913fcbcdbe8f80d6c1fe5fce3bb49e1f0040a943</id>
    <comment>
      Fix TST-23: 2-phase load components
    </comment>
    <repositoryName>hg</repositoryName>
    <repositoryType>Mercurial</repositoryType>
    <additional>14</additional>
    <buildId>321</buildId>

    <modifications>
      <modification>
        <action>MODIFY</action>
        <path>Test.java</path>
        <edition>913fcbcdbe8f80d6c1fe5fce3bb49e1f0040a943</edition>
        <previousEdition>f090cd04725c5551f8a439fe0a53591193ea79c3</previousEdition>
        <additional>14</additional>
      </modification>
      <modification>
        <action>MODIFY</action>
        <path>big.java</path>
        <edition>913fcbcdbe8f80d6c1fe5fce3bb49e1f0040a943</edition>
        <previousEdition>f090cd04725c5551f8a439fe0a53591193ea79c3</previousEdition>
        <additional>14</additional>
      </modification>
    </modifications>
  </changeset>
</list>
"""


@responses.activate
def test_get_version(client):
    responses.add(
        responses.GET,
        re.compile(r'.*/rest/changes/version'),
        content_type='text/plain',
        body='3.2',
    )

    version = client.changes.get_version()
    assert version == '3.2'


@responses.activate
def test_get_commit_stats(client):
    responses.add(
        responses.GET,
        re.compile(r'.*/rest/changes/stats/.+'),
        content_type='text/xml',
        body='<stats commits="5" modifications="7" added="2" modified="3" deleted="2"/>',
    )

    stats = client.changes.get_commit_stats(
        1,
        build=9,
        from_build=1,
        to_build=333,
        from_date='19911209',
        to_date='20211209',
        date_pattern='yyyyMMdd',
        repository='main',
        committer='p.belskiy',
    )

    assert stats['commits'] == 5
    assert stats['modifications'] == 7
    assert stats['added'] == 2
    assert stats['modified'] == 3
    assert stats['deleted'] == 2


@responses.activate
def test_get_changesets(client):
    responses.add(
        responses.GET,
        re.compile(r'.*/rest/changes/.+'),
        content_type='text/xml',
        body=CHANGESETS_XML,
    )

    changesets = client.changes.get_changesets(
        1,
        build=9,
        from_build=1,
        to_build=333,
        from_date='19911209',
        to_date='20211209',
        date_pattern='yyyyMMdd',
        repository='main',
        committer='p.belskiy',
        offset=1,
        limit=100,
        asc=False,
    )

    assert changesets[0]['user'] == 'steve'


@responses.activate
def test_get_build_commits_changesets(client):
    responses.add(
        responses.GET,
        re.compile(r'.*/rest/changes/commits/build/.+'),
        content_type='text/xml',
        body=CHANGESETS_XML,
    )

    changesets = client.changes.get_build_commits_changesets(123)
    assert changesets[0]['user'] == 'steve'


@responses.activate
def test_get_build_stats_changesets(client):
    responses.add(
        responses.GET,
        re.compile(r'.*/rest/changes/stats/build/.+'),
        content_type='text/xml',
        body=CHANGESETS_XML,
    )

    changesets = client.changes.get_build_stats_changesets(123)
    assert changesets[0]['user'] == 'steve'
