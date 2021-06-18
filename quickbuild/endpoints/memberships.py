from functools import partial
from typing import List, Optional, Union

from quickbuild.helpers import ContentType, response2py


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

    def get_info(self,
                 membership_id: int,
                 *,
                 content_type: Optional[ContentType] = None
                 ) -> Union[dict, str]:
        """
        Get full membership info.

        Args:
            membership_id (int):
                Membership identifier.

            content_type (Optional[ContentType]):
                Select needed content type if not set, default value of client
                instance is used.

        Returns:
            Union[str, dict]: membership content.
        """
        return self.quickbuild._request(
            'GET',
            'memberships/{}'.format(membership_id),
            callback=partial(response2py, content_type=content_type),
            content_type=content_type,
        )

    def get_by_user(self, user_id: int) -> Union[List[dict], str]:
        """
        Get memberships of particular user.

        Args:
            user_id (int): user identifier.

        Returns:
            Union[List[dict], str]: user membership content.
        """
        return self.quickbuild._request(
            'GET',
            'memberships',
            params=dict(user_id=user_id),
            callback=response2py,
        )

    def get_by_group(self, group_id: int) -> Union[List[dict], str]:
        """
        Get memberships of particular group.

        Args:
            group_id (int): group identifier.

        Returns:
            Union[List[dict], str]: group membership content.
        """
        return self.quickbuild._request(
            'GET',
            'memberships',
            params=dict(group_id=group_id),
            callback=response2py,
        )
