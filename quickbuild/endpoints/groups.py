from functools import partial
from typing import List, Optional, Union

from quickbuild.exceptions import QBError
from quickbuild.helpers import response2py


class Groups:

    def __init__(self, quickbuild):
        self.quickbuild = quickbuild

    def get(self) -> List[dict]:
        """
        Get all groups in the system.

        Returns:
            List[dict]: list of groups.
        """
        return self.quickbuild._request(
            'GET',
            'groups',
            callback=response2py
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
        return self.quickbuild._request(
            'GET',
            'groups/{}'.format(group_id),
            callback=partial(response2py, as_xml=as_xml)
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
        return self.quickbuild._request(
            'POST',
            'groups',
            callback=response2py,
            data=configuration
        )

    def create(self, configuration: str) -> int:
        """
        Create a group using XML configuration.

        Normally you do not need to create the XML from scratch: you may retrieve
        XML representation of a templating group using `get_info(as_xml=True)`
        remove the id element, modify certain parts and use i XML as configuration
        for create method.

        Args:
            configuration (str): XML document.

        Returns:
            int: group id being created.

        Raises:
            QBError: XML validation error
        """
        if '</id>' in configuration:
            raise QBError('`id` element must not be in XML for create method')

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
            callback=response2py,
        )
