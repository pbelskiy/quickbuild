from typing import List

from quickbuild.helpers import response2py


class Authorizations:

    def __init__(self, quickbuild):
        self.quickbuild = quickbuild

    def get(self) -> List[dict]:
        """
        Get all authorizations in the system.

        Returns:
            List[dict]: list of all authorizations in the system.
        """
        return self.quickbuild._request(
            'GET',
            'authorizations',
            callback=response2py,
        )

    def get_info(self, authorization_id: int) -> dict:
        """
        Get authorization info by id.

        Returns:
            dict: authorization info.
        """
        return self.quickbuild._request(
            'GET',
            'authorizations/{}'.format(authorization_id),
            callback=response2py,
        )

    def get_by_group(self, group_id: int) -> dict:
        """
        Get authorization info by group id.

        Returns:
            dict: authorization info.
        """
        params = dict(group_id=group_id)

        return self.quickbuild._request(
            'GET',
            'authorizations',
            callback=response2py,
            params=params,
        )

    def get_by_configuration(self, configuration_id: int) -> dict:
        """
        Get authorization info by configuration_id.

        Returns:
            dict: authorization info.
        """
        params = dict(configuration_id=configuration_id)

        return self.quickbuild._request(
            'GET',
            'authorizations',
            callback=response2py,
            params=params,
        )

    def update(self, configuration: str) -> int:
        """
        Update an authorization using XML configuration.

        Normally you do not need to create the XML from scratch: you may retrieve
        XML representation of the authorization using http GET method, modify
        certain parts of the XML and post back to above url.

        Args:
            configuration (str): XML document.

        Returns:
            int: authorization id being updated.
        """
        return self.quickbuild._request(
            'POST',
            'authorizations',
            callback=response2py,
            data=configuration
        )
