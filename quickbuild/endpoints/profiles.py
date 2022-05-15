from typing import List

from quickbuild.helpers import response2py


class Profiles:

    def __init__(self, quickbuild):
        self.quickbuild = quickbuild

    def get(self) -> List[dict]:
        """
        Get all cloud profiles in the system.

        Returns:
            List[dict]: list of users.
        """
        return self.quickbuild._request(
            'GET',
            'cloud_profiles',
            callback=response2py
        )
