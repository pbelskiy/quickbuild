import re

from http import HTTPStatus

import pytest
import responses

from quickbuild import ContentType, QBClient, QBError, QBServerError
from quickbuild.exceptions import QBForbiddenError

GET_VERSION_DATA = '6.0.9'


USERS_XML = r"""<?xml version="1.0" encoding="UTF-8"?>

<list>
  <com.pmease.quickbuild.model.User>
    <id>1</id>
    <favoriteDashboardIds>
      <long>1</long>
    </favoriteDashboardIds>
    <name>admin</name>
    <lastLogin>2021-06-10T14:18:21.292Z</lastLogin>
    <password secret="hash">0DPiKuNIrrVmD8IUCuw1hQxNqZc=</password>
    <pluginSettingDOMs/>
  </com.pmease.quickbuild.model.User>
  <com.pmease.quickbuild.model.User>
    <id>2</id>
    <favoriteDashboardIds/>
    <name>pbelskiy</name>
    <lastLogin>2021-06-07T14:24:49.066Z</lastLogin>
    <password secret="hash">je+glP0P8AYzGoaLZE16xTSJKC8=</password>
    <pluginSettingDOMs/>
  </com.pmease.quickbuild.model.User>
</list>
"""

USERS_JSON = """[ {
  "@class" : "com.pmease.quickbuild.model.User",
  "id" : 1,
  "favoriteDashboardIds" : [ 1 ],
  "name" : "admin",
  "lastLogin" : "2021-06-10T14:18:21.292+00:00",
  "password" : {
    "value" : "0DPiKuNIrrVmD8IUCuw1hQxNqZc=",
    "secret" : "hash"
  },
  "pluginSettingDOMs" : { }
}, {
  "@class" : "com.pmease.quickbuild.model.User",
  "id" : 2,
  "favoriteDashboardIds" : [ ],
  "name" : "pbelskiy",
  "lastLogin" : "2021-06-07T14:24:49.066+00:00",
  "password" : {
    "value" : "je+glP0P8AYzGoaLZE16xTSJKC8=",
    "secret" : "hash"
  },
  "pluginSettingDOMs" : { }
} ]
"""


@responses.activate
def test_content_type_parse_get():
    responses.add(
        responses.GET,
        re.compile(r'.*/rest/users'),
        content_type='application/xml',
        body=USERS_XML,
    )

    client = QBClient('http://server', content_type=ContentType.PARSE)

    users = client.users.get()
    assert isinstance(users, list)


@responses.activate
def test_content_type_xml_get():
    responses.add(
        responses.GET,
        re.compile(r'.*/rest/users'),
        content_type='application/xml',
        body=USERS_XML,
    )

    client = QBClient('http://server', content_type=ContentType.XML)

    users = client.users.get()
    assert isinstance(users, str)


@responses.activate
def test_content_type_json_get():
    responses.add(
        responses.GET,
        re.compile(r'.*/rest/users'),
        content_type='application/json',
        body=USERS_JSON,
    )

    client = QBClient('http://server', content_type=ContentType.JSON)

    users = client.users.get()
    assert isinstance(users, list)


@responses.activate
def test_content_type_headers_sync_json_json():

    def callback(request):
        assert request.headers['Accept'] == 'application/json'
        return (HTTPStatus.OK, request.headers, request.body)

    responses.add_callback(
        responses.GET,
        re.compile(r'.*/rest/memberships/\d+'),
        callback=callback
    )

    client = QBClient('http://server', content_type=ContentType.JSON)
    client.memberships.get_info(1)


@responses.activate
def test_content_type_headers_sync_xml_json():

    def callback(request):
        assert request.headers['Accept'] == 'application/json'
        return (HTTPStatus.OK, request.headers, request.body)

    responses.add_callback(
        responses.GET,
        re.compile(r'.*/rest/memberships/\d+'),
        callback=callback
    )

    client = QBClient('http://server', content_type=ContentType.XML)
    client.memberships.get_info(1, content_type=ContentType.JSON)


@responses.activate
def test_content_type_headers_sync_json_xml():

    def callback(request):
        assert request.headers['Accept'] == '*/*'
        return (HTTPStatus.OK, request.headers, request.body)

    responses.add_callback(
        responses.GET,
        re.compile(r'.*/rest/memberships/\d+'),
        callback=callback
    )

    client = QBClient('http://server', content_type=ContentType.JSON)
    client.memberships.get_info(1, content_type=ContentType.XML)


@responses.activate
def test_exception_server_error(client):
    responses.add(
        responses.GET,
        re.compile(r'.*/rest/version'),
        body=GET_VERSION_DATA,
        status=HTTPStatus.INTERNAL_SERVER_ERROR
    )

    with pytest.raises(QBServerError):
        client.system.get_version()


@responses.activate
def test_exception_forbidden_error(client):
    responses.add(
        responses.GET,
        re.compile(r'.*/rest/version'),
        body=GET_VERSION_DATA,
        status=HTTPStatus.FORBIDDEN
    )

    with pytest.raises(QBForbiddenError):
        client.system.get_version()


@responses.activate
def test_exception_common_error(client):
    responses.add(
        responses.GET,
        re.compile(r'.*/rest/version'),
        body=GET_VERSION_DATA,
        status=HTTPStatus.METHOD_NOT_ALLOWED
    )
    with pytest.raises(QBError):
        client.system.get_version()
