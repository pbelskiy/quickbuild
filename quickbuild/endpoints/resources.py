from typing import List

from quickbuild.helpers import response2py


class Resources:

    def __init__(self, quickbuild):
        self.quickbuild = quickbuild

    def get(self) -> List[dict]:
        """
        Get all resources in the system.

        Returns:
            List[dict]: list of resources.
        """
        return self.quickbuild._request(
            'GET',
            'resources',
            callback=response2py,
        )

    def get_by_id(self, resource_id: int) -> dict:
        """
        Get resource by identifier.

        Args:
            resource_id (int):
                Identifier of a resources.

        Returns:
            dict: resource.
        """
        return self.quickbuild._request(
            'GET',
            'resources/{}'.format(resource_id),
            callback=response2py,
        )

    def get_total_count(self, resource_id: int) -> int:
        """
        Get total resource count across nodes.

        Args:
            resource_id (int):
                Identifier of a resources.

        Returns:
            int: total resources count.
        """
        return self.quickbuild._request(
            'GET',
            'resources/{}/total'.format(resource_id),
            callback=response2py,
        )

    def get_available_count(self, resource_id: int) -> int:
        """
        Get available resource count across nodes.

        Args:
            resource_id (int):
                Identifier of a resources.

        Returns:
            int: total resources count.
        """
        return self.quickbuild._request(
            'GET',
            'resources/{}/available'.format(resource_id),
            callback=response2py,
        )

    def update(self, configuration: str) -> int:
        """
        Update resource.

        Normally you do not need to create the configuration from scratch,
        you may retrieve configuration representation of the resource using
        get_*() methods, modify certain parts and use it as new configuration.

        Args:
            configuration (str):
                Resource configuration.

        Returns:
            int: resource id being updated.
        """
        return self.quickbuild._request(
            'POST',
            'resources',
            callback=response2py,
            data=configuration,
        )

    def create(self, configuration: str) -> int:
        """
        Create resource.

        Please note that the posted configuration should NOT contain the id
        element, otherwise, QuickBuild will treat the post as an updating to
        the resource with that id.

        Normally you do not need to create the configuration from scratch:
        you may retrieve configuration representation of a templating resource
        using get_*() methods, remove the id element, modify certain parts
        and use it as new configuration.

        Args:
            configuration (str):
                Resource configuration.

        Returns:
            int: resource id being created.
        """
        return self.update(configuration)

    def delete(self, resource_id: int) -> None:
        """
        Delete resource.

        Args:
            resource_id (int):
                Identifier of a resources.

        Returns:
            None
        """
        return self.quickbuild._request(
            'DELETE',
            'resources/{}'.format(resource_id),
            callback=response2py,
        )
