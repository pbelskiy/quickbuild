from typing import List

import xmltodict


class Users:

    def __init__(self, quickbuild):
        self.quickbuild = quickbuild

    def get(self) -> List[dict]:
        """
        Get all users in the system.

        Returns:
            List[dict]: list of users.
        """
        def callback(response: str) -> List[dict]:
            root = xmltodict.parse(response)
            users = root['list']['com.pmease.quickbuild.model.User']
            if isinstance(users, list) is False:
                users = [users]
            return users

        return self.quickbuild._request(
            'GET',
            'users',
            callback
        )

    def get_info(self, user_id: int) -> dict:
        """
        Get information about specified user.

        Args:
            user_id (int): user identifier.

        Returns:
            dict: information about user.
        """
        def callback(response: str) -> dict:
            root = xmltodict.parse(response)
            return root['com.pmease.quickbuild.model.User']

        return self.quickbuild._request(
            'GET',
            'users/{}'.format(user_id),
            callback
        )

    def get_display_name(self, user_id: int) -> str:
        """
        Get display name for specified user.

        Returns:
            str: user name.
        """
        return self.quickbuild._request(
            'GET',
            'users/{}/display_name'.format(user_id)
        )
