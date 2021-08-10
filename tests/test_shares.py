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
def test_get_user_share_by_dashboard_id(client):
    responses.add(
        responses.GET,
        re.compile(r'.*/rest/user_shares'),
        content_type='application/xml',
        body=USER_SHARES_XML,
    )

    response = client.shares.users.get_by_dashboard_id(1)
    assert response[0]['user'] == 2


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
