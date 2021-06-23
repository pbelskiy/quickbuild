import re

import responses

from quickbuild import ContentType

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

USER_MEMBERSHIPS_XML = r"""<?xml version="1.0" encoding="UTF-8"?>

<list>
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

GROUP_MEMBERSHIPS_XML = r"""<?xml version="1.0" encoding="UTF-8"?>

<list>
  <com.pmease.quickbuild.model.Membership>
    <id>2</id>
    <user>2</user>
    <group>1</group>
    <assignedLocally>true</assignedLocally>
  </com.pmease.quickbuild.model.Membership>
</list>
"""

CREATE_MEMBERSHIP_XML = r"""<?xml version="1.0" encoding="UTF-8"?>

<com.pmease.quickbuild.model.Membership>
  <!-- id of associated user of this membership. -->
  <user>2</user>

  <!-- id of associated group of this membership. -->
  <group>1</group>
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

    response = client.memberships.get_info(1, content_type=ContentType.XML)
    assert '<com.pmease.quickbuild.model.Membership>' in response


@responses.activate
def test_get_by_user(client):
    responses.add(
        responses.GET,
        re.compile(r'.*/rest/memberships'),
        content_type='application/xml',
        body=USER_MEMBERSHIPS_XML,
    )

    response = client.memberships.get_by_user(2)
    assert len(response) == 2
    assert response[0]['id'] == 2
    assert response[0]['group'] == 1
    assert response[0]['assignedLocally'] is True


@responses.activate
def test_get_by_group(client):
    responses.add(
        responses.GET,
        re.compile(r'.*/rest/memberships'),
        content_type='application/xml',
        body=GROUP_MEMBERSHIPS_XML,
    )

    response = client.memberships.get_by_group(1)
    assert len(response) == 1
    assert response[0]['id'] == 2
    assert response[0]['user'] == 2
    assert response[0]['group'] == 1
    assert response[0]['assignedLocally'] is True


@responses.activate
def test_update(client):
    responses.add(
        responses.POST,
        re.compile(r'.*/rest/memberships'),
        content_type='application/xml',
        body='3',
    )

    response = client.memberships.update(USER_MEMBERSHIPS_XML)
    assert response == 3


@responses.activate
def test_create(client):
    responses.add(
        responses.POST,
        re.compile(r'.*/rest/memberships'),
        content_type='application/xml',
        body='5',
    )

    response = client.memberships.create(CREATE_MEMBERSHIP_XML)
    assert response == 5


@responses.activate
def test_delete(client):
    responses.add(
        responses.DELETE,
        re.compile(r'.*/rest/memberships'),
    )

    response = client.memberships.delete(100)
    assert response is None
