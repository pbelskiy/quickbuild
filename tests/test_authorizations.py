import re

import responses

AUTHORIZATIONS_XML = r"""<?xml version="1.0" encoding="UTF-8"?>

<list>
  <com.pmease.quickbuild.model.Authorization>
    <group>3</group>
    <configuration>3</configuration>
    <permissions>
      <string>RUN_BUILD</string>
      <string>STOP_BUILD</string>
    </permissions>
  </com.pmease.quickbuild.model.Authorization>
</list>
"""

AUTHORIZATION_XML = r"""<?xml version="1.0" encoding="UTF-8"?>

<com.pmease.quickbuild.model.Authorization>
  <group>3</group>
  <configuration>3</configuration>
  <permissions>
    <string>RUN_BUILD</string>
    <string>STOP_BUILD</string>
  </permissions>
</com.pmease.quickbuild.model.Authorization>
"""


@responses.activate
def test_get(client):
    responses.add(
        responses.GET,
        re.compile(r'.*/rest/authorizations'),
        content_type='application/xml',
        body=AUTHORIZATIONS_XML,
    )

    response = client.authorizations.get()
    assert len(response) == 1
    assert response[0]['group'] == 3


@responses.activate
def test_get_info(client):
    responses.add(
        responses.GET,
        re.compile(r'.*/rest/authorizations/\d+'),
        content_type='application/xml',
        body=AUTHORIZATION_XML,
    )

    response = client.authorizations.get_info(3)
    assert response['configuration'] == 3


@responses.activate
def test_get_by_group(client):
    responses.add(
        responses.GET,
        re.compile(r'.*/rest/authorizations'),
        content_type='application/xml',
        body=AUTHORIZATION_XML,
    )

    response = client.authorizations.get_by_group(3)
    assert response['group'] == 3


@responses.activate
def test_get_by_configuration(client):
    responses.add(
        responses.GET,
        re.compile(r'.*/rest/authorizations'),
        content_type='application/xml',
        body=AUTHORIZATION_XML,
    )

    response = client.authorizations.get_by_configuration(1)
    assert response['group'] == 3


@responses.activate
def test_update(client):
    responses.add(
        responses.POST,
        re.compile(r'.*/rest/authorizations'),
        content_type='application/xml',
        body='123',
    )

    response = client.authorizations.update(AUTHORIZATION_XML)
    assert response == 123


@responses.activate
def test_create(client):
    responses.add(
        responses.POST,
        re.compile(r'.*/rest/authorizations'),
        content_type='application/xml',
        body='123',
    )

    response = client.authorizations.create(AUTHORIZATION_XML)
    assert response == 123


@responses.activate
def test_delete(client):
    responses.add(
        responses.DELETE,
        re.compile(r'.*/rest/authorizations'),
        content_type='text/plain',
    )

    assert client.authorizations.delete(1) is None
