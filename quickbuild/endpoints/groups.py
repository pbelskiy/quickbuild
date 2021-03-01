from typing import List

import xmltodict


class Groups:

    def __init__(self, quickbuild):
        self.quickbuild = quickbuild

    def get(self) -> List[dict]:
        """
        Get all groups in the system.

        Returns:
            List[dict]: list of groups.
        """
        def callback(response: str) -> List[dict]:
            root = xmltodict.parse(response)
            groups = root['list']['com.pmease.quickbuild.model.Group']
            if isinstance(groups, list) is False:
                groups = [groups]
            return groups

        return self.quickbuild._request(
            'GET',
            'groups',
            callback
        )

    def get_info(self, group_id: int) -> dict:
        """
        Get information about specified group.

        Args:
            group_id (int): group identifier.

        Returns:
            dict: group information.
        """
        def callback(response: str) -> dict:
            root = xmltodict.parse(response)
            return root['com.pmease.quickbuild.model.Group']

        return self.quickbuild._request(
            'GET',
            'groups/{}'.format(group_id),
            callback
        )
