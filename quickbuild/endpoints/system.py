from typing import NamedTuple

import xmltodict

from quickbuild.exceptions import QBError

ServerVersion = NamedTuple(
    'ServerVersion', [('major', int), ('minor', int), ('patch', int)]
)


class System:

    def __init__(self, quickbuild):
        self.quickbuild = quickbuild

    def get_version(self) -> ServerVersion:
        """
        Show server version information.

        Returns:
            ServerVersion: NamedTuple with major, minor and patch version.
        """
        def callback(response: str) -> ServerVersion:
            return ServerVersion(*map(int, response.split('.')))

        return self.quickbuild._request('GET', 'version', callback)

    def pause(self) -> None:
        """
        Pause system.

        Raises:
            QBError: if system haven`t paused.
        """
        def callback(response: str) -> None:
            if response != 'paused':
                raise QBError(response)

        return self.quickbuild._request('GET', 'pause', callback)

    def resume(self) -> None:
        """
        Resumed system.

        Raises:
            QBError: if system haven`t resumed.
        """
        def callback(response: str) -> None:
            if response != 'resumed':
                raise QBError(response)

        return self.quickbuild._request('GET', 'resume', callback)

    def get_pause_information(self) -> None:
        """
        Get system pause information including pause reason.

        Returns:
            ServerVersion: NamedTuple with major, minor and patch version.

        Raises:
            QBProcessingError: will be raised if system is not paused.
        """
        def callback(response: str) -> None:
            root = xmltodict.parse(response)
            return root['com.pmease.quickbuild.setting.system.PauseSystem']

        return self.quickbuild._request('GET', 'paused', callback)

    def backup(self, configuration: str) -> str:
        """
        Backup database using XML configuration.

        Args:
            configuration (str): XML document.

        Returns:
            str: Absolute path to the backup file.
        """
        return self.quickbuild._request('POST', 'backup', data=configuration)
