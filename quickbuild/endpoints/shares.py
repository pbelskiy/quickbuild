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

    https://wiki.pmease.com/display/QB10/Interact+with+User+Share
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

    def update(self, configuration: str) -> int:
        """
        Update user share using XML configuration.

        Normally you do not need to create the XML from scratch: you may retrieve
        XML representation of the share, modify certain parts of the XML and post
        back to above url.

        Args:
            configuration (str): XML document.

        Returns:
            int: user share id being updated.
        """
        return self.quickbuild._request(
            'POST',
            'user_shares',
            callback=response2py,
            data=configuration
        )

    def create(self, configuration: str) -> int:
        """
        Create user share using XML configuration.

        Normally you do not need to create the XML from scratch: you may retrieve
        XML representation of the share, modify certain parts of the XML and post
        back to above url.

        Args:
            configuration (str): XML document.

        Returns:
            int: user share id being created.
        """
        return self.update(configuration)

    def delete(self, share_id: str) -> None:
        """
        Delete the user share.

        Args:
            share_id (int):
                Share identifier.

        Returns:
            int: user share id being deleted.
        """
        return self.quickbuild._request(
            'DELETE',
            'user_shares/{}'.format(share_id),
            callback=response2py,
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

    def get_by_id(self, share_id: int) -> Union[dict, str]:
        """
        Get group share by identifier.

        Args:
            share_id (int):
                Share identifier.

        Returns:
            Union[dict, str]: user share.
        """
        return self.quickbuild._request(
            'GET',
            'group_shares/{}'.format(share_id),
            callback=response2py
        )

    def get_by_dashboard_id(self, dashboard_id: int) -> Union[List[dict], str]:
        """
        Get group shares by dashboard identifier.

        Args:
            dashboard_id (int):
                Dashboard identifier.

        Returns:
            Union[List[dict], str]: list of group shares.
        """
        return self.quickbuild._request(
            'GET',
            'group_shares',
            callback=response2py,
            params=dict(dashboard_id=dashboard_id),
        )

    def get_by_group_id(self, group_id: int) -> Union[List[dict], str]:
        """
        Get group shares by group identifier.

        Args:
            group_id (int):
                Represents id of the group to query group share information for.
                Particularly, use id 0 to query group shares targeting everyone.

        Returns:
            Union[List[dict], str]: list of group shares.
        """
        return self.quickbuild._request(
            'GET',
            'group_shares',
            callback=response2py,
            params=dict(group_id=group_id),
        )

    def update(self, configuration: str) -> int:
        """
        Update group share using XML configuration.

        Normally you do not need to create the XML from scratch: you may retrieve
        XML representation of the share, modify certain parts of the XML and post
        back to above url.

        Args:
            configuration (str): XML document.

        Returns:
            int: group share id being updated.
        """
        return self.quickbuild._request(
            'POST',
            'group_shares',
            callback=response2py,
            data=configuration
        )

    def create(self, configuration: str) -> int:
        """
        Create group share using XML configuration.

        Normally you do not need to create the XML from scratch: you may retrieve
        XML representation of the share, modify certain parts of the XML and post
        back to above url.

        Args:
            configuration (str): XML document.

        Returns:
            int: group share id being updated.
        """
        return self.update(configuration)

    def delete(self, share_id: str) -> None:
        """
        Delete group share.

        Args:
            share_id (int):
                Share identifier.

        Returns:
            int: group share id being deleted.
        """
        return self.quickbuild._request(
            'DELETE',
            'group_shares/{}'.format(share_id),
            callback=response2py,
        )
