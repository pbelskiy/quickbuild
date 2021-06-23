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

    def update(self, configuration: str) -> int:
        """
        Update membership using XML/JSON representation of the membership.

        Normally you do not need to create the representation from scratch, you
        may retrieve XML/JSON representation of the membership using `get_info()`
        method, modify certain parts and use it as new representation for update.

        Demo:
        -----
        1. Assume id of user robin is 2, id of group developer is 1, and id of
           group tester is 2.
        2. Get memberships of user robin using `get_by_user(2)` method.
        3. Analyze response of above command to find out the membership with
           group id.
        4. Modify response and change the group element to use value of 2.
        5. Use it as new membership membership to this `update()` method.

        Args:
            representation (str): representation of membership.

        Returns:
            int: membership id being updated.
        """
        return self.quickbuild._request(
            'POST',
            'memberships',
            callback=response2py,
            data=configuration,
        )

    def create(self, configuration: str) -> int:
        """
        Create membership using XML/JSON representation of the membership.

        Normally you do not need to create the representation from scratch, you
        may retrieve XML/JSON representation of the membership using `get_info()`
        method, modify certain parts and use it as new representation for create.

        Demo:
        -----
        How to add user robin (assume id is 2) to group tester (assume the id is 3).

        .. code-block:: xml
            <com.pmease.quickbuild.model.Membership>
              <user>2</user>
              <group>3</group>
            </com.pmease.quickbuild.model.Membership>

        Args:
            representation (str): representation of membership.

        Returns:
            int: newly created membership id.
        """
        return self.update(configuration)

    def delete(self, membership_id: int) -> None:
        """
        Delete membership.

        Demo:
        -----
        1. User robin (assume id is 2) from group tester (assume the id is 3).
        2. Get memberships of user robin with `get_by_user(2)`
        3. Analyze response of above command to find out id of the membership
           associated with group id 3, assume id of the found membership is 100.
        4. Delete the found membership id 100.

        Args:
            membership_id (str): membership identifier.
        """
        return self.quickbuild._request(
            'DELETE',
            'memberships/{}'.format(membership_id),
            callback=response2py,
        )
