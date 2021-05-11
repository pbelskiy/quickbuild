import re

import responses

AUDITS_XML = r"""<?xml version="1.0" encoding="UTF-8"?>

<list>
  <com.pmease.quickbuild.model.Audit>
    <id>47</id>
    <user>Anonymous</user>
    <timestamp>2021-05-10T07:11:32.285Z</timestamp>
    <configuration>7</configuration>
    <action>Build request was submitted by scheduler.</action>
  </com.pmease.quickbuild.model.Audit>
  <com.pmease.quickbuild.model.Audit>
    <id>46</id>
    <user>Anonymous</user>
    <timestamp>2021-05-10T07:11:20.336Z</timestamp>
    <configuration>3</configuration>
    <action>Build request was submitted by scheduler.</action>
  </com.pmease.quickbuild.model.Audit>
  <com.pmease.quickbuild.model.Audit>
    <id>45</id>
    <user>Anonymous</user>
    <timestamp>2021-05-10T07:11:14.315Z</timestamp>
    <configuration>1</configuration>
    <action>Build request was submitted by scheduler.</action>
  </com.pmease.quickbuild.model.Audit>
</list>
"""


@responses.activate
def test_get(client):
    responses.add(
        responses.GET,
        re.compile(r'.*/rest/audits'),
        content_type='application/xml',
        body=AUDITS_XML,
    )

    response = client.audits.get(
      count=3,
      username='Anonymous',
      source='root',
      action='Build request was submitted by scheduler.',
      since='2010-01-01',
      until='2022-01-01',
      first=45,
    )

    assert len(response) == 3
    assert response[1]['id'] == 46
    assert response[1]['configuration'] == 3


@responses.activate
def test_count(client):
    responses.add(
        responses.GET,
        re.compile(r'.*/rest/audits/count'),
        body='11',
    )

    response = client.audits.count()
    assert response == 11
