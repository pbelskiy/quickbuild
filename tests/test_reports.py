import re

import responses

CATEGORIES_XML = r"""
<list>
  <string>unprocessed</string>
  <string>tests</string>
  <string>testsuites</string>
  <string>packages</string>
  <string>stats</string>
  <string>agg_overview</string>
  <string>agg_stats</string>
  <string>tests_trends</string>
</list>
"""

DEFINITION_XML = r"""
<meta name="stats" group="STATISTICS">
  <column name="ID" isKey="false" indexed="false" nullable="false" updatable="false" sqlType="BIGINT" dataType="ID"/>
  <column name="buildId" isKey="true" indexed="false" nullable="true" updatable="true" sqlType="BIGINT" dataType="ID"/>
  <column name="duration" isKey="false" indexed="false" nullable="true" updatable="true" sqlType="BIGINT" dataType="DURATION"/>
  <column name="tests" isKey="false" indexed="false" nullable="true" updatable="true" sqlType="INT" dataType="INTEGER"/>
  ... ...
</meta>
"""

AGGREGATIONS_XML = r"""
<list>
  <string>DEFAULT</string>
  <string>On Linux</string>
  <string>On Windows</string>
</list>
"""


@responses.activate
def test_get_version(client):
    responses.add(
        responses.GET,
        re.compile(r'.*/rest/junit/version'),
        content_type='text/plain',
        body='2.1',
    )

    version = client.reports.get_tracker('junit').get_version()
    assert version == '2.1'


@responses.activate
def test_get_categories(client):
    responses.add(
        responses.GET,
        re.compile(r'.*/rest/junit/reports'),
        content_type='application/xml',
        body=CATEGORIES_XML,
    )

    categories = client.reports.get_tracker('junit').get_categories()
    assert len(categories) == 8
    assert categories[0] == 'unprocessed'


@responses.activate
def test_get_definition(client):
    responses.add(
        responses.GET,
        re.compile(r'.*/rest/junit/meta/stats'),
        content_type='application/xml',
        body=DEFINITION_XML,
    )

    definition = client.reports.get_tracker('junit').get_definition('stats')
    assert definition['name'] == 'stats'
    assert definition['column'][0]['name'] == 'ID'


@responses.activate
def test_get_aggregations(client):
    responses.add(
        responses.GET,
        re.compile(r'.*/rest/junit/reportsets/BUILD/103'),
        content_type='application/xml',
        body=AGGREGATIONS_XML,
    )

    aggregations = client.reports.get_tracker('junit').get_aggregations('BUILD', 103)
    assert len(aggregations) == 3
    assert aggregations[0] == 'DEFAULT'
