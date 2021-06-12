import re

import responses

MEMBERSHIPS_XML = r"""<?xml version="1.0" encoding="UTF-8"?>

<list>
  <com.pmease.quickbuild.model.Membership>
    <id>1</id>
    <user>1</user>
    <group>2</group>
    <assignedLocally>true</assignedLocally>
  </com.pmease.quickbuild.model.Membership>
  <com.pmease.quickbuild.model.Membership>
    <id>2</id>
    <user>2</user>
    <group>1</group>
    <assignedLocally>true</assignedLocally>
  </com.pmease.quickbuild.model.Membership>
  <com.pmease.quickbuild.model.Membership>
    <id>3</id>
    <user>2</user>
    <group>2</group>
    <assignedLocally>true</assignedLocally>
  </com.pmease.quickbuild.model.Membership>
</list>
"""

MEMBERSHIP_INFO_XML = r"""<?xml version="1.0" encoding="UTF-8"?>

<com.pmease.quickbuild.model.Membership>
  <id>1</id>
  <user>1</user>
  <group>2</group>
  <assignedLocally>true</assignedLocally>
</com.pmease.quickbuild.model.Membership>
"""


@responses.activate
def test_get(client):
    responses.add(
        responses.GET,
        re.compile(r'.*/rest/memberships'),
        content_type='application/xml',
        body=MEMBERSHIPS_XML,
    )

    response = client.memberships.get()
    assert len(response) == 3
    assert response[0]['id'] == 1
    assert response[1]['group'] == 1
    assert response[2]['assignedLocally'] is True


@responses.activate
def test_get_info(client):
    responses.add(
        responses.GET,
        re.compile(r'.*/rest/memberships/\d+'),
        content_type='application/xml',
        body=MEMBERSHIP_INFO_XML,
    )

    response = client.memberships.get_info(1)
    assert response['id'] == 1
    assert response['group'] == 2
    assert response['assignedLocally'] is True

    response = client.memberships.get_info(1, as_xml=True)
    assert '<com.pmease.quickbuild.model.Membership>' in response