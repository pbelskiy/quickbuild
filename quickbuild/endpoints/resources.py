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
