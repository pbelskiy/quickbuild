from typing import List, Union

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

    def get_info(self, cloud_profile_id: int) -> Union[dict, str]:
        """
        Get information about cloud profile.

        Returns:
            dict: information cloud profile.
        """
        return self.quickbuild._request(
            'GET',
            'cloud_profiles/{}'.format(cloud_profile_id),
            callback=response2py,
        )
