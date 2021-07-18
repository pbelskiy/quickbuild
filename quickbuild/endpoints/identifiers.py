from typing import Any

from quickbuild.helpers import response2py


class Identifiers:
    """
    Most of QuickBuild RESTful API relies on identifier of the object,
    which can be retrieved with the id service explained here.

    https://wiki.pmease.com/display/QB10/Retrieve+Object+Identifier
    """
    def __init__(self, quickbuild):
        self.quickbuild = quickbuild

    def _get(self, params: dict) -> Any:
        return self.quickbuild._request(
            'GET',
            'ids',
            callback=response2py,
            params=params,
        )

    def get_resource_id_by_name(self, name: str) -> int:
        """
        Get resource id by name.

        **This feature is available since 6.1.35**

        Args:
            name (str): resource path.

        Returns:
            int: resource identifier.

        Raises:
            QBProcessingError: will be raised if resource is not found.
        """
        return self._get(dict(resource_name=name))

    def get_configuration_id_by_path(self, path: str) -> int:
        """
        Get configuration id by path.

        Args:
            path (str): configuration path.

        Returns:
            int: configuration identifier.

        Raises:
            QBProcessingError: will be raised if resource is not found.
        """
        return self._get(dict(configuration_path=path))

    def get_user_id_by_name(self, name: str) -> int:
        """
        Get user id by name.

        Args:
            name (str): user name.

        Returns:
            int: user identifier.

        Raises:
            QBProcessingError: will be raised if resource is not found.
        """
        return self._get(dict(user_name=name))

    def get_group_id_by_name(self, name: str) -> int:
        """
        Get group id by name.

        Args:
            name (str): group name.

        Returns:
            int: group identifier.

        Raises:
            QBProcessingError: will be raised if resource is not found.
        """
        return self._get(dict(group_name=name))

    def get_queue_id_by_name(self, name: str) -> int:
        """
        Get queue id by name.

        Args:
            name (str): queue name.

        Returns:
            int: queue identifier.

        Raises:
            QBProcessingError: will be raised if resource is not found.
        """
        return self._get(dict(queue_name=name))

    def get_build_id_by_request_id(self, identifier: int) -> int:
        """
        Get build id by request id.

        Args:
            identifier (int): request identifier.

        Returns:
            int: build identifier.

        Raises:
            QBProcessingError: will be raised if resource is not found.
        """
        return self._get(dict(request_id=identifier))

    def get_build_id_by_build_name(self, name: str) -> int:
        """
        Get build id by build name.

        For example how to get id of latest build in configuration with id 1,
        name will be `1.latest`

        Args:
            name (str): build name.

        Returns:
            int: build identifier.

        Raises:
            QBProcessingError: will be raised if resource is not found.
        """
        return self._get(dict(build_name=name))

    def get_dashboard_id_by_dashboard_fqn(self, fqn: str) -> int:
        """
        Get dashboard id by dashboard fqn (fully qualified name).

        <dashboard fqn> is of the form <user id>.<dashboard name>.

        Args:
            fqn (str): fqn (fully qualified name).

        Returns:
            int: dashboard identifier.

        Raises:
            QBProcessingError: will be raised if resource is not found.
        """
        return self._get(dict(dashboard_fqn=fqn))
