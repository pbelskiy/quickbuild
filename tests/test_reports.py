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
