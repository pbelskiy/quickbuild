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

    def get_info(self, authorization_id: int) -> dict:
        """
        Get authorization info by id.

        Returns:
            dict: authorization info.
        """
        return self.quickbuild._request(
            'GET',
            'authorizations/{}'.format(authorization_id),
            callback=response2py,
        )

    def get_by_group(self, group_id: int) -> dict:
        """
        Get authorization info by group id.

        Returns:
            dict: authorization info.
        """
        params = dict(group_id=group_id)

        return self.quickbuild._request(
            'GET',
            'authorizations',
            callback=response2py,
            params=params,
        )
