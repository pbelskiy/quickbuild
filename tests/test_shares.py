import re

import responses

USER_SHARES_XML = r"""<?xml version="1.0" encoding="UTF-8"?>

<list>
  <com.pmease.quickbuild.model.UserShare>
    <id>1</id>
    <user>2</user>
    <dashboard>1</dashboard>
  </com.pmease.quickbuild.model.UserShare>
  <com.pmease.quickbuild.model.UserShare>
    <id>2</id>
    <user>1</user>
    <dashboard>1</dashboard>
  </com.pmease.quickbuild.model.UserShare>
</list>
"""

USER_SHARE_XML = r"""<?xml version="1.0" encoding="UTF-8"?>

<com.pmease.quickbuild.model.UserShare>
  <id>1</id>
  <user>2</user>
  <dashboard>1</dashboard>
</com.pmease.quickbuild.model.UserShare>
"""

GROUP_SHARES_XML = r"""<?xml version="1.0" encoding="UTF-8"?>

<list>
  <com.pmease.quickbuild.model.GroupShare>
    <id>1</id>
    <group>2</group>
    <dashboard>1</dashboard>
  </com.pmease.quickbuild.model.GroupShare>
  <com.pmease.quickbuild.model.GroupShare>
    <id>2</id>
    <group>1</group>
    <dashboard>1</dashboard>
  </com.pmease.quickbuild.model.GroupShare>
</list>
"""

GROUP_SHARE_XML = r"""<?xml version="1.0" encoding="UTF-8"?>

<com.pmease.quickbuild.model.GroupShare>
  <id>1</id>
  <group>2</group>
  <dashboard>1</dashboard>
</com.pmease.quickbuild.model.GroupShare>
"""


@responses.activate
def test_get_user_shares(client):
    responses.add(
        responses.GET,
        re.compile(r'.*/rest/user_shares'),
        content_type='application/xml',
        body=USER_SHARES_XML,
    )

    response = client.shares.users.get()
    assert len(response) == 2
    assert response[0]['user'] == 2
    assert client.shares.users.get() == client.users.shares.get()


@responses.activate
def test_get_user_share_by_id(client):
    responses.add(
        responses.GET,
        re.compile(r'.*/rest/user_shares/1'),
        content_type='application/xml',
        body=USER_SHARE_XML,
    )

    response = client.shares.users.get_by_id(1)
    assert response['user'] == 2
    assert client.shares.users.get_by_id(1) == client.users.shares.get_by_id(1)


@responses.activate
def test_get_user_shares_by_dashboard_id(client):
    responses.add(
        responses.GET,
        re.compile(r'.*/rest/user_shares'),
        content_type='application/xml',
        body=USER_SHARES_XML,
    )

    response = client.shares.users.get_by_dashboard_id(1)
    assert response[0]['user'] == 2


@responses.activate
def test_get_user_shares_by_user_id(client):
    responses.add(
        responses.GET,
        re.compile(r'.*/rest/user_shares'),
        content_type='application/xml',
        body=USER_SHARES_XML,
    )

    response = client.shares.users.get_by_user_id(1)
    assert response[0]['user'] == 2


@responses.activate
def test_update_user_share(client):
    responses.add(
        responses.POST,
        re.compile(r'.*/rest/user_shares'),
        body='123',
    )

    response = client.shares.users.update(USER_SHARE_XML)
    assert response == 123


@responses.activate
def test_create_user_share(client):
    responses.add(
        responses.POST,
        re.compile(r'.*/rest/user_shares'),
        body='124',
    )

    response = client.shares.users.create(USER_SHARE_XML)
    assert response == 124


@responses.activate
def test_delete_user_share(client):
    responses.add(
        responses.DELETE,
        re.compile(r'.*/rest/user_shares/.+'),
    )

    client.shares.users.delete(124)


""" ################################ GROUPS ################################ """


@responses.activate
def test_get_group_shares(client):
    responses.add(
        responses.GET,
        re.compile(r'.*/rest/group_shares'),
        content_type='application/xml',
        body=GROUP_SHARES_XML,
    )

    response = client.shares.groups.get()
    assert len(response) == 2
    assert response[0]['group'] == 2
    assert client.shares.groups.get() == client.groups.shares.get()


@responses.activate
def test_get_group_share_by_id(client):
    responses.add(
        responses.GET,
        re.compile(r'.*/rest/group_shares'),
        content_type='application/xml',
        body=GROUP_SHARE_XML,
    )

    response = client.shares.groups.get_by_id(15)
    assert response['id'] == 1
    assert client.shares.groups.get_by_id(15) == client.groups.shares.get_by_id(15)


@responses.activate
def test_get_group_shares_by_dashboard_id(client):
    responses.add(
        responses.GET,
        re.compile(r'.*/rest/group_shares'),
        content_type='application/xml',
        body=GROUP_SHARES_XML,
    )

    response = client.shares.groups.get_by_dashboard_id(1)
    assert len(response) == 2
    assert response[0]['group'] == 2
    assert client.shares.groups.get() == client.groups.shares.get()


@responses.activate
def test_get_group_shares_by_group_id(client):
    responses.add(
        responses.GET,
        re.compile(r'.*/rest/group_shares'),
        content_type='application/xml',
        body=GROUP_SHARES_XML,
    )

    response = client.shares.groups.get_by_group_id(1)
    assert len(response) == 2
    assert response[0]['group'] == 2
    assert client.shares.groups.get() == client.groups.shares.get()


@responses.activate
def test_update_group_share(client):
    responses.add(
        responses.POST,
        re.compile(r'.*/rest/group_shares'),
        body='123',
    )

    response = client.shares.groups.update(GROUP_SHARE_XML)
    assert response == 123


@responses.activate
def test_create_group_share(client):
    responses.add(
        responses.POST,
        re.compile(r'.*/rest/group_shares'),
        body='123',
    )

    response = client.shares.groups.create(GROUP_SHARE_XML)
    assert response == 123


@responses.activate
def test_delete_group_share(client):
    responses.add(
        responses.DELETE,
        re.compile(r'.*/rest/group_shares/.+'),
    )

    client.shares.groups.delete(124)
