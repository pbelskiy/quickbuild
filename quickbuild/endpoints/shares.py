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
