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
