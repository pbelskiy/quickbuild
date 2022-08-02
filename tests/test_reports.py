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

BUILD_STATS_XML = r"""
<report name="stats" version="0.0.0" locale="en_US">
  <row ID="1" buildId="103" duration="261466" tests="1006" errors="5" failures="7" skips="0"
   added="994" newFailed="12" notFixed="0" fixed="0" successes="994" success_rate="0.9880715705765407"/>
</report>
"""

RECORDS_DATA_XML = r"""<report name="tests" version="0.0" locale="en_US">
  <row ID="100" packageName="org.hibernate.test.entitymode.multi" className="MultiRepresentationTest"
       testName="testPojoRetreival" status="PASS" duration="40" hasSysout="true" totalRuns="2"
       failedRuns="0" passedRuns="2" diffStatus="ADDED"/>
  <row ID="101" packageName="org.hibernate.test.entitymode.multi" className="MultiRepresentationTest"
       testName="testDom4jRetreival" status="PASS" duration="58" hasSysout="true" totalRuns="2"
       failedRuns="0" passedRuns="2" diffStatus="FIXED"/>
  <row ID="102" packageName="org.hibernate.test.entitymode.multi" className="MultiRepresentationTest"
       testName="testDom4jSave" status="PASS" duration="34" hasSysout="true" totalRuns="2"
       failedRuns="0" passedRuns="2" diffStatus="FIXED"/>
  <row ID="103" packageName="org.hibernate.test.entitymode.multi" className="MultiRepresentationTest"
       testName="testDom4jHQL" status="PASS" duration="30" hasSysout="true" totalRuns="2"
       failedRuns="0" passedRuns="2" diffStatus="ADDED"/>
</report>
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


@responses.activate
def test_get_build_stats(client):
    responses.add(
        responses.GET,
        re.compile(r'.*/rest/junit/buildstats/103/DEFAULT'),
        content_type='application/xml',
        body=BUILD_STATS_XML,
    )

    stats = client.reports.get_tracker('junit').get_build_stats(103, 'DEFAULT')
    assert stats['row']['duration'] == 261466


@responses.activate
def test_get_records_size(client):
    responses.add(
        responses.GET,
        re.compile(r'.*/rest/junit/size/tests/103/DEFAULT'),
        content_type='text/plain',
        body='5',
    )

    size = client.reports.get_tracker('junit').get_records_size(
        'tests',
        103,
        'DEFAULT'
    )

    assert size == 5


@responses.activate
def test_get_records_data(client):
    responses.add(
        responses.GET,
        re.compile(r'.*/rest/junit/records/tests/103/DEFAULT'),
        content_type='application/xml',
        body=RECORDS_DATA_XML,
    )

    data = client.reports.get_tracker('junit').get_records_data(
        'tests',
        103,
        'DEFAULT'
    )['row']

    assert len(data) == 4
    assert data[0]['testName'] == 'testPojoRetreival'
