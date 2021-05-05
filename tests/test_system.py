import re

from http import HTTPStatus

import pytest
import responses

from quickbuild import QBError, QBProcessingError


@responses.activate
def test_pause_success(client):
    responses.add(
        responses.GET,
        re.compile(r'.*/rest/pause'),
        body='paused'
    )

    client.system.pause()


@responses.activate
def test_pause_error(client):
    responses.add(
        responses.GET,
        re.compile(r'.*/rest/pause'),
        body='error'
    )

    with pytest.raises(QBError):
        client.system.pause()


@responses.activate
def test_resume_success(client):
    responses.add(
        responses.GET,
        re.compile(r'.*/rest/resume'),
        body='resumed'
    )

    client.system.resume()


@responses.activate
def test_resume_error(client):
    responses.add(
        responses.GET,
        re.compile(r'.*/rest/resume'),
        body='paused'
    )

    with pytest.raises(QBError):
        client.system.resume()


@responses.activate
def test_get_pause_information_success(client):
    BODY = r"""<?xml version="1.0" encoding="UTF-8"?>

    <com.pmease.quickbuild.setting.system.PauseSystem>
      <user>admin</user>
    </com.pmease.quickbuild.setting.system.PauseSystem>
    """

    responses.add(
        responses.GET,
        re.compile(r'.*/rest/paused'),
        body=BODY
    )

    info = client.system.get_pause_information()
    assert info['user'] == 'admin'


@responses.activate
def test_get_pause_information_error(client):
    responses.add(
        responses.GET,
        re.compile(r'.*/rest/paused'),
        status=HTTPStatus.NO_CONTENT,
    )

    with pytest.raises(QBProcessingError):
        client.system.get_pause_information()


@responses.activate
def test_backup(client):
    CONFIGURATION = r"""
    <com.pmease.quickbuild.web.page.administration.BackupNowOption>
      <!-- Destination file for the backup -->
      <backupTo>/path/to/backup.zip</backupTo>

      <!-- Whether or not to exclude builds in the backup -->
      <excludeBuilds>false</excludeBuilds>

      <!-- Whether or not to exclude measurement data in the backup -->
      <excludeMeasurements>false</excludeMeasurements>

      <!-- Whether or not to exclude audits in the backup -->
      <excludeAudits>false</excludeAudits>

      <!-- Whether or not to clear passwords in the backup -->
      <clearPasswords>false</clearPasswords>
    </com.pmease.quickbuild.web.page.administration.BackupNowOption>
    """

    responses.add(
        responses.POST,
        re.compile(r'.*/rest/backup'),
        body='/tmp/backup.zip'
    )

    assert client.system.backup(CONFIGURATION) == '/tmp/backup.zip'
