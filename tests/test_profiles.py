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

CLOUD_PROFILE_XML = r"""<?xml version="1.0" encoding="UTF-8"?>

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
        body=CLOUD_PROFILE_XML,
    )

    response = client.profiles.get_info(1)
    assert response['id'] == 1
