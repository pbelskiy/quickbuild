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
