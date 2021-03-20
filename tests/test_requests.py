import re

import responses

from quickbuild import QBClient

REQUEST_XML = r"""<?xml version="1.0" encoding="UTF-8"?>

<list>
  <com.pmease.quickbuild.BuildRequest>
    <configurationId>1</configurationId>
    <respectBuildCondition>false</respectBuildCondition>
    <variables/>
    <upstreamRequestIds/>
    <id>ad6d09d9-56ef-4c5e-9a56-fd98f34255a1</id>
    <priority>5</priority>
    <requestDate>2021-03-20T21:19:53.779Z</requestDate>
    <requesterId>1</requesterId>
    <scheduled>false</scheduled>
    <status>RUNNING_BUILD</status>
  </com.pmease.quickbuild.BuildRequest>
  <com.pmease.quickbuild.BuildRequest>
    <configurationId>1</configurationId>
    <respectBuildCondition>false</respectBuildCondition>
    <variables/>
    <upstreamRequestIds/>
    <id>5ef67a04-652d-47ae-82e5-40258e23ee26</id>
    <priority>5</priority>
    <requestDate>2021-03-20T21:19:54.017Z</requestDate>
    <requesterId>1</requesterId>
    <scheduled>false</scheduled>
    <status>WAITING_PROCESS</status>
  </com.pmease.quickbuild.BuildRequest>
</list>
"""


@responses.activate
def test_get():
    responses.add(
        responses.GET,
        re.compile(r'.*/rest/build_requests'),
        body=REQUEST_XML,
        content_type='application/xml',
    )

    response = QBClient('http://server').requests.get(
        configuration_id=1,
        trigger_user_id=1
    )

    assert len(response) == 2
    assert response[0]['id'] == 'ad6d09d9-56ef-4c5e-9a56-fd98f34255a1'
    assert response[1]['status'] == 'WAITING_PROCESS'
