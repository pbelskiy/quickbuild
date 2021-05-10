from typing import List, Optional, Union

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

    def get_info(self,
                 group_id: int,
                 *,
                 as_xml: Optional[bool] = False
                 ) -> Union[dict, str]:
        """
        Get information about specified group.

        Args:
            group_id (int): group identifier.

        Returns:
            dict: group information.
        """
        def callback(response: str) -> Union[dict, str]:
            if as_xml:
                return response

            root = xmltodict.parse(response)
            return root['com.pmease.quickbuild.model.Group']

        return self.quickbuild._request(
            'GET',
            'groups/{}'.format(group_id),
            callback
        )

    def update(self, configuration: str) -> int:
        """
        Update a group using XML configuration.

        Normally you do not need to create the XML from scratch: you may retrieve
        XML representation of the group using `get_info()` method, modify certain
        parts of the XML and post back to above url.

        Args:
            configuration (str): XML document.

        Returns:
            int: group id being updated.
        """
        def callback(response: str) -> int:
            return int(response)

        return self.quickbuild._request(
            'POST',
            'groups',
            callback,
            data=configuration
        )

    def create(self, configuration: str) -> int:
        """
        Create a group using XML configuration.

        Please note that the posted XML should NOT contain the id element;
        otherwise, QuickBuild will treat the post as an updating to the group
        with that id. Normally you do not need to create the XML from scratch:
        you may retrieve XML representation of a templating group using `get_info()`
        method, remove the id element, modify certain parts and post back to
        above url.

        Args:
            configuration (str): XML document.

        Returns:
            int: group id being created.
        """
        return self.update(configuration)

    def delete(self, group_id: int) -> None:
        """
        Delete specified group.

        Args:
            group_id (int): group identifier.

        Returns:
            int: group id being created.
        """
        return self.quickbuild._request(
            'DELETE',
            'groups/{}'.format(group_id),
        )
