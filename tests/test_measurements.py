import re

import responses

MEASUREMENTS_GET_XML = r"""<?xml version="1.0" encoding="UTF-8"?>

<list>
  <com.pmease.quickbuild.model.MeasurementDataR00>
    <id>335</id>
    <timestamp>1361854800000</timestamp>
    <source>Zhenyu-MBP.local:8810</source>
    <metricName>web.rpc.oneMinuteRate</metricName>
    <value>10.3903417298681</value>
  </com.pmease.quickbuild.model.MeasurementDataR00>
  <com.pmease.quickbuild.model.MeasurementDataR00>
    <id>334</id>
    <timestamp>1361854800000</timestamp>
    <source>Zhenyu-MBP.local:8810</source>
    <metricName>web.rpc.fiveMinuteRate</metricName>
    <value>8.90793420070343</value>
  </com.pmease.quickbuild.model.MeasurementDataR00>
</list>
"""


@responses.activate
def test_get(client):
    responses.add(
        responses.GET,
        re.compile(r'.*/rest/grid/measurements'),
        content_type='application/xml',
        body=MEASUREMENTS_GET_XML,
    )

    response = client.measurements.get(
        source='Zhenyu-MBP.local:8810',
        period='LAST_2_HOURS',
        start_time='2013/02/25+09:47',
        end_time='2013/02/27+09:47',
        metric='web.rpc.fiveMinuteRate',
        date_pattern='yyyy/MM/dd+HH:mm',
    )

    assert len(response) == 2
    assert response[0]['id'] == 335


@responses.activate
def test_get_version(client):
    responses.add(
        responses.GET,
        re.compile(r'.*/rest/grid/measurements/version'),
        content_type='application/xml',
        body='6.0',
    )

    response = client.measurements.get_version()
    assert response == '6.0'
