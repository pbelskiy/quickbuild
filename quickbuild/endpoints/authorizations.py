from typing import List

from quickbuild.helpers import response2py


class Authorizations:

    def __init__(self, quickbuild):
        self.quickbuild = quickbuild

    def get(self) -> List[dict]:
        """
        Get all authorizations in the system.

        Returns:
            List[dict]: list of all authorizations in the system.
        """
        return self.quickbuild._request(
            'GET',
            'authorizations',
            callback=response2py,
        )
