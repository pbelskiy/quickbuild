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
