from typing import List

from quickbuild.helpers import response2py


class Memberships:

    def __init__(self, quickbuild):
        self.quickbuild = quickbuild

    def get(self) -> List[dict]:
        """
        Get all memberships in the system.

        Returns:
            List[dict]: list of all memberships.
        """
        return self.quickbuild._request(
            'GET',
            'memberships',
            callback=response2py,
        )
