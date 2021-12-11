import re

import responses


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
