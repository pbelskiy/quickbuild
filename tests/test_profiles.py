import re

import pytest
import responses

from quickbuild import QBError

CLOUD_PROFILES_LIST_XML = r"""<?xml version="1.0" encoding="UTF-8"?>

<list>
  <com.pmease.quickbuild.model.CloudProfile>
    <id>1</id>
  </com.pmease.quickbuild.model.CloudProfile>
</list>
"""

CLOUD_PROFILE_INFO_XML = r"""<?xml version="1.0" encoding="UTF-8"?>

<com.pmease.quickbuild.model.CloudProfile>
  <id>1</id>
</com.pmease.quickbuild.model.CloudProfile>
"""


@responses.activate
def test_get(client):
    responses.add(
        responses.GET,
        re.compile(r'.*/rest/cloud_profiles'),
        content_type='application/xml',
        body=CLOUD_PROFILES_LIST_XML,
    )

    response = client.profiles.get()
    assert len(response) == 1
    assert response[0]['id'] == 1


@responses.activate
def test_get_info(client):
    responses.add(
        responses.GET,
        re.compile(r'.*/rest/cloud_profiles/1'),
        content_type='application/xml',
        body=CLOUD_PROFILE_INFO_XML,
    )

    response = client.profiles.get_info(1)
    assert response['id'] == 1


@responses.activate
def test_update(client):
    responses.add(
        responses.POST,
        re.compile(r'.*/rest/cloud_profiles'),
        body='1991',
    )

    response = client.profiles.update(CLOUD_PROFILE_INFO_XML)
    assert response == 1991


@responses.activate
def test_create(client):
    responses.add(
        responses.POST,
        re.compile(r'.*/rest/cloud_profiles'),
        body='1991',
    )

    xml_with_id = CLOUD_PROFILE_INFO_XML
    xml_without_id = xml_with_id.replace('<id>1</id>', '')

    with pytest.raises(QBError):
        client.profiles.create(xml_with_id)

    response = client.profiles.create(xml_without_id)
    assert response == 1991


@responses.activate
def test_delete(client):
    responses.add(
        responses.DELETE,
        re.compile(r'.*/rest/cloud_profiles/\d'),
    )

    response = client.profiles.delete(9)
    assert response is None
