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
