from typing import List, Union

from quickbuild.helpers import response2py


class Shares:
    """
    Share is the object used to control dashboard sharing with users or groups.
    """
    def __init__(self, quickbuild):
        self.users = UserShares(quickbuild)
        self.groups = GroupShares(quickbuild)


class UserShares:
    """
    User share is the object used to control dashboard sharing with users.
    """
    def __init__(self, quickbuild):
        self.quickbuild = quickbuild

    def get(self) -> Union[List[dict], str]:
        """
        Get all user shares in the system.

        Returns:
            Union[List[dict], str]: list of all user shares.
        """
        return self.quickbuild._request(
            'GET',
            'user_shares',
            callback=response2py
        )

    def get_by_id(self, share_id: int) -> Union[dict, str]:
        """
        Get user share by identifier.

        Args:
            share_id (int):
                Share identifier.

        Returns:
            Union[dict, str]: user share.
        """
        return self.quickbuild._request(
            'GET',
            'user_shares/{}'.format(share_id),
            callback=response2py
        )

    def get_by_dashboard_id(self, dashboard_id: int) -> Union[List[dict], str]:
        """
        Get user shares by dashboard identifier.

        Args:
            dashboard_id (int):
                Dashboard identifier.

        Returns:
            Union[List[dict], str]: list of user shares.
        """
        return self.quickbuild._request(
            'GET',
            'user_shares',
            callback=response2py,
            params=dict(dashboard_id=dashboard_id),
        )

    def get_by_user_id(self, user_id: int) -> Union[List[dict], str]:
        """
        Get user shares by user identifier.

        Args:
            user_id (int):
                User identifier.

        Returns:
            Union[List[dict], str]: list of user shares.
        """
        return self.quickbuild._request(
            'GET',
            'user_shares',
            callback=response2py,
            params=dict(user_id=user_id),
        )


class GroupShares:
    """
    Group share is the object used to control dashboard sharing with groups.
    """
    def __init__(self, quickbuild):
        self.quickbuild = quickbuild

    def get(self) -> Union[List[dict], str]:
        """
        Get all group shares in the system.

        Returns:
            Union[List[dict], str]: list of all group shares.
        """
        return self.quickbuild._request(
            'GET',
            'group_shares',
            callback=response2py
        )
