import re

import responses

GET_REQUEST_XML = r"""<?xml version="1.0" encoding="UTF-8"?>

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

CREATE_REQUEST_XML = r"""
<com.pmease.quickbuild.BuildRequest>
  <!-- This element tells QuickBuild in what configuration to trigger build. -->
  <configurationId>10</configurationId>

  <!-- This element tells whether or not to respect build condition of the configuration.
       If this is set to true, and if the build condition evaluates to false, build will
       not be triggered. -->
  <respectBuildCondition>false</respectBuildCondition>

  <!-- This optional element specifies priority of the build request, with value ranging from 1 to 10. The
  bigger this value is, the higher the priority is -->
  <priority>10</priority>

  <!-- This element is optional and is used to specify variables for build triggering. If
       specified, it will override the variable with the same name defined in configuration
       basic setting. -->
  <variables>
    <entry>
      <string>var_name1</string>
      <string>var_value1</string>
    </entry>
    <entry>
      <string>var_name2</string>
      <string>var_value2</string>
    </entry>
  </variables>

  <!-- This element is optional and is used to tell QuickBuild to request a build promotion. -->
  <promotionSource>

    <!-- This element is optional and is used to tell QuickBuild that the source build resides on another
         QuickBuild server. -->
    <server>
      <url>http://another-qb-server:8810</url>
      <userName>admin</userName>
      <password>admin</password>
    </server>

    <!-- Identifier of the source build to promote from -->
    <buildId>697</buildId>

    <!-- This element is optional and used to specify files to promote -->
    <deliveries>
      <com.pmease.quickbuild.FileDelivery>
        <srcPath>artifacts/dir1</srcPath>
        <filePatterns>**/*.jar</filePatterns>
      </com.pmease.quickbuild.FileDelivery>
      <com.pmease.quickbuild.FileDelivery>
        <srcPath>artifacts/dir2</srcPath>
        <filePatterns>**/*.war</filePatterns>
      </com.pmease.quickbuild.FileDelivery>
    </deliveries>
  </promotionSource>

</com.pmease.quickbuild.BuildRequest>
"""

CREATE_REQUEST_RESULT_XML = r"""<?xml version="1.0" encoding="UTF-8"?>
<com.pmease.quickbuild.RequestResult>
    <requestId>e8e5fb23-7aff-4efd-9825-162eeac84fca</requestId>
    <loopedRequest>false</loopedRequest>
</com.pmease.quickbuild.RequestResult>
"""


@responses.activate
def test_get(client):
    responses.add(
        responses.GET,
        re.compile(r'.*/rest/build_requests'),
        body=GET_REQUEST_XML,
        content_type='application/xml',
    )

    response = client.requests.get(
        configuration_id=1,
        trigger_user_id=1
    )

    assert len(response) == 2
    assert response[0]['id'] == 'ad6d09d9-56ef-4c5e-9a56-fd98f34255a1'
    assert response[1]['status'] == 'WAITING_PROCESS'


@responses.activate
def test_create(client):
    CREATE_REQUEST_RESULT_XML = r"""<?xml version="1.0" encoding="UTF-8"?>
    <com.pmease.quickbuild.RequestResult>
        <requestId>e8e5fb23-7aff-4efd-9825-162eeac84fca</requestId>
        <loopedRequest>false</loopedRequest>
    </com.pmease.quickbuild.RequestResult>
    """

    responses.add(
        responses.POST,
        re.compile(r'.*/rest/build_requests'),
        body=CREATE_REQUEST_RESULT_XML,
    )

    response = client.requests.create(CREATE_REQUEST_XML)
    assert response['requestId'] == 'e8e5fb23-7aff-4efd-9825-162eeac84fca'


@responses.activate
def test_trigger(client):
    responses.add(
        responses.GET,
        re.compile(r'.*/rest/trigger'),
        body=CREATE_REQUEST_RESULT_XML,
    )

    response = client.requests.trigger(10)
    assert response['requestId'] == 'e8e5fb23-7aff-4efd-9825-162eeac84fca'


@responses.activate
def test_delete(client):
    responses.add(
        responses.DELETE,
        re.compile(r'.*/rest/build_requests'),
    )

    client.requests.delete('e8e5fb23-7aff-4efd-9825-162eeac84fca')
