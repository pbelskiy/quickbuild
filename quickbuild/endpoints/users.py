from functools import partial
from typing import List, Optional, Union

from quickbuild.endpoints.shares import UserShares
from quickbuild.helpers import ContentType, response2py


class Users:

    def __init__(self, quickbuild):
        self.quickbuild = quickbuild

        self.shares = UserShares(quickbuild)

    def get(self) -> List[dict]:
        """
        Get all users in the system.

        Returns:
            List[dict]: list of users.
        """
        return self.quickbuild._request(
            'GET',
            'users',
            callback=response2py
        )

    def get_info(self,
                 user_id: int,
                 *,
                 content_type: Optional[ContentType] = None
                 ) -> Union[dict, str]:
        """
        Get information about specified user.

        Args:
            user_id (int):
                User identifier.

            content_type (Optional[ContentType]):
                Select needed content type if not set, default value of client
                instance is used.

        Returns:
            dict: information about user.
        """
        return self.quickbuild._request(
            'GET',
            'users/{}'.format(user_id),
            callback=partial(response2py, content_type=content_type),
            content_type=content_type,
        )

    def get_display_name(self, user_id: int) -> str:
        """
        Get display name for specified user.

        Args:
            user_id (int): user identifier.

        Returns:
            str: user name.
        """
        return self.quickbuild._request(
            'GET',
            'users/{}/display_name'.format(user_id)
        )

    def get_id_by_name(self, name: str) -> int:
        """
        Get user id by name.

        Args:
            name (str): user name.

        Returns:
            int: user identifier.

        Raises:
            QBProcessingError: will be raised if resource is not found.
        """
        return self.quickbuild.identifiers.get_user_id_by_name(name)

    def update(self, configuration: str) -> int:
        """
        Update user using XML configuration.

        Normally you do not need to create the xml from scratch: you may retrieve
        XML representation of the user using ``get_info()`` method, modify certain
        parts of the XML and post back to above url.

        Args:
            configuration (str): XML document.

        Returns:
            int: user id being updated.
        """
        return self.quickbuild._request(
            'POST',
            'users',
            callback=response2py,
            data=configuration,
        )

    def create(self, configuration: str) -> int:
        """
        Create a new user using XML/JSON configuration.

        Normally you do not need to create the XML from scratch: you may
        retrieve XML representation of a templating user using ``get_info()``,
        remove the id element, modify certain parts and use it.

        Args:
            configuration (str): XML/JSON document.

        Returns:
            int: id of the newly created user.

        Raises:
            QBError: configuration validation error.
        """
        self.quickbuild._validate_for_id(configuration)
        return self.update(configuration)

    def delete(self, user_id: int) -> None:
        """
        Delete user by user id.

        Args:
            user_id (int): user identifier.

        Returns:
            None
        """
        return self.quickbuild._request(
            'DELETE',
            'users/{}'.format(user_id),
            callback=response2py,
        )
