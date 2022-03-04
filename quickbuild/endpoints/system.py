from typing import NamedTuple

from quickbuild.exceptions import QBError
from quickbuild.helpers import response2py

ServerVersion = NamedTuple(
    'ServerVersion', [
        ('major', int),
        ('minor', int),
        ('patch', int),
        ('qualifier', str),
    ]
)


class System:

    def __init__(self, quickbuild):
        self.quickbuild = quickbuild

    def get_version(self) -> ServerVersion:
        """
        Show server version information.

        Returns:
            ServerVersion: major, minor, patch version and qualifier.
        """
        def callback(response: str) -> ServerVersion:
            if '-' in response:
                version, qualifier = response.split('-')
            else:
                version, qualifier = response, ''

            major, minor, patch = version.split('.')

            return ServerVersion(
                major=int(major),
                minor=int(minor),
                patch=int(patch) if patch.isnumeric() else 0,
                qualifier=qualifier,
            )

        return self.quickbuild._request(
            'GET',
            'version',
            callback=callback
        )

    def pause(self) -> None:
        """
        Pause system.

        Raises:
            QBError: system has not paused.
        """
        def callback(response: str) -> None:
            if response != 'paused':
                raise QBError(response)

        return self.quickbuild._request(
            'GET',
            'pause',
            callback=callback
        )

    def resume(self) -> None:
        """
        Resume system.

        Raises:
            QBError: system has not resumed.
        """
        def callback(response: str) -> None:
            if response != 'resumed':
                raise QBError(response)

        return self.quickbuild._request(
            'GET',
            'resume',
            callback=callback
        )

    def get_pause_information(self) -> str:
        """
        Get system pause information including pause reason.

        Returns:
            str: pause information.

        Raises:
            QBProcessingError: will be raised if system is not paused.
        """
        return self.quickbuild._request(
            'GET',
            'paused',
            callback=response2py
        )

    def backup(self, configuration: str) -> str:
        """
        Backup database using XML configuration.

        Args:
            configuration (str): XML document.

        Returns:
            str: Absolute path to the backup file.
        """
        return self.quickbuild._request(
            'POST',
            'backup',
            data=configuration
        )
