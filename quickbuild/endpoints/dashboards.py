from typing import List

from quickbuild.helpers import response2py


class Dashboards:

    def __init__(self, quickbuild):
        self.quickbuild = quickbuild

    def get(self) -> List[dict]:
        """
        Get all dashboards in the system.

        Returns:
            List[dict]: list of all dashboards.
        """
        return self.quickbuild._request(
            'GET',
            'dashboards',
            callback=response2py,
        )
