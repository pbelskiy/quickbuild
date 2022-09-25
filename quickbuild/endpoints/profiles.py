from typing import List, Optional, Union

from quickbuild.helpers import ContentType, response2py


class Profiles:

    def __init__(self, quickbuild) -> None:
        self.quickbuild = quickbuild

    def get(self) -> List[dict]:
        """
        Get all cloud profiles in the system.

        Returns:
            List[dict]: list of users.
        """
        return self.quickbuild._request(
            'GET',
            'cloud_profiles',
            callback=response2py
        )

    def get_info(self,
                 cloud_profile_id: int,
                 *,
                 content_type: Optional[ContentType] = None
                 ) -> Union[dict, str]:
        """
        Get information about cloud profile.

        Args:
            cloud_profile_id (int):
                Cloud profile identifier.

            content_type (Optional[ContentType]):
                Select needed content type if not set, default value of client
                instance is used.

        Returns:
            Union[dict, str]: information cloud profile.
        """
        return self.quickbuild._request(
            'GET',
            'cloud_profiles/{}'.format(cloud_profile_id),
            callback=response2py,
            content_type=content_type
        )

    def update(self, configuration: str) -> int:
        """
        Update a cloud profile using XML configuration.

        Normally you do not need to create the XML from scratch: you may get
        XML representation of the configuration using `get_info()` method with
        content_type=ContentType.XML and modify certain parts of the XML.

        Args:
            configuration (str):
                XML document.

        Returns:
            int: cloud profile id being updated.
        """
        return self.quickbuild._request(
            'POST',
            'cloud_profiles',
            callback=response2py,
            data=configuration
        )

    def create(self, configuration: str) -> int:
        """
        Create a cloud profile using XML/JSON configuration.

        Please note that:

        The posted XML should NOT contain the id element; otherwise, QuickBuild
        will treat the post as an updating to the cloud profile with that id.
        Normally you do not need to create the XML from scratch: you may retrieve
        XML representation of a templating cloud profile using `get_info()` method,
        remove the id element, modify certain parts and post back to above url.

        Args:
            configuration (str):
                XML/JSON document.

        Returns:
            int: id of newly created cloud profile.

        Raises:
            QBError: XML validation error
        """
        self.quickbuild._validate_for_id(configuration)
        return self.update(configuration)

    def delete(self, cloud_profile_id: int) -> None:
        """
        Delete cloud profile.

        Args:
            cloud_profile_id (int):
                Cloud profile id.

        Returns:
            None
        """
        return self.quickbuild._request(
            'DELETE',
            'cloud_profiles/{}'.format(cloud_profile_id),
            callback=response2py,
        )
