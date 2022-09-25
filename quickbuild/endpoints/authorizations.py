from typing import List, Optional, Union

from quickbuild.helpers import ContentType, response2py


class Authorizations:

    def __init__(self, quickbuild) -> None:
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

    def get_info(self,
                 authorization_id: int,
                 *,
                 content_type: Optional[ContentType] = None
                 ) -> Union[dict, str]:
        """
        Get authorization info by id.

        Args:
            authorization_id (int):
                Authorization identifier.

            content_type (Optional[ContentType]):
                Select needed content type if not set, default value of client
                instance is used.

        Returns:
            Union[dict, str]: authorization info.
        """
        return self.quickbuild._request(
            'GET',
            'authorizations/{}'.format(authorization_id),
            callback=response2py,
            content_type=content_type,
        )

    def get_by_group(self, group_id: int) -> dict:
        """
        Get authorization info by group id.

        Args:
            group_id (int):
                Group identifier.

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

        Args:
            configuration_id (int):
                Configuration identifier.

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
            configuration (str):
                XML document.

        Returns:
            int: authorization id being updated.
        """
        return self.quickbuild._request(
            'POST',
            'authorizations',
            callback=response2py,
            data=configuration
        )

    def create(self, configuration: str) -> int:
        """
        Create an authorization using XML/JSON configuration.

        Please note that: posted XML should NOT contain the id element; otherwise
        QuickBuild will treat the post as an updating to the authorization with
        that id. Normally you do not need to create the XML from scratch: you may
        retrieve XML representation of a templating authorization using http GET
        method, remove the id element, modify certain parts and post back to above
        url.

        Args:
            configuration (str):
                XML/JSON document.

        Returns:
            int: newly created authorizations id.

        Raises:
            QBError: XML validation error
        """
        self.quickbuild._validate_for_id(configuration)
        return self.update(configuration)

    def delete(self, configuration_id: int) -> None:
        """
        Delete authorization by configuration_id.

        Args:
            configuration_id (int):
                Configuration identifier.

        Returns:
            None
        """
        return self.quickbuild._request(
            'DELETE',
            'authorizations/{}'.format(configuration_id),
            callback=response2py,
        )
