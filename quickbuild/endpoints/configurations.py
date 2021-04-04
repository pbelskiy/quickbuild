from typing import List, Optional, Union

import xmltodict


class Configurations:

    def __init__(self, quickbuild):
        self.quickbuild = quickbuild

    def _get(self, params: dict) -> List[dict]:

        def callback(response: str) -> List[dict]:
            root = xmltodict.parse(response)
            configurations = root['list']['com.pmease.quickbuild.model.Configuration']
            if isinstance(configurations, list) is False:
                configurations = [configurations]
            return configurations

        return self.quickbuild._request(
            'GET',
            'configurations',
            callback,
            params=params,
        )

    def get(self) -> List[dict]:
        """
        Get all configurations in the system. For performance reason, only
        brief  information of the configuration will be returned here, including
        `id`, `name`, `description`, `schedule`, `runMode`, `errorMessage`,
        `parent id`. You may get the full xml representation using id if necessary.

        Returns:
            List[dict]: list of configurations.
        """
        return self._get(dict(recursive=True))

    def get_child(self, parent_id: int) -> List[dict]:
        """
        Get a list of child configurations.

        Args:
            parent_id (int): parent configuration identifier.

        Returns:
            List[dict]: list of child configurations.
        """
        return self._get(dict(parent_id=parent_id))

    def get_descendent(self, parent_id: int) -> List[dict]:
        """
        Get a list of descendent configurations.

        Args:
            parent_id (int): parent configuration identifier.

        Returns:
            List[dict]: list of descendent configurations.
        """
        return self._get(dict(recursive=True, parent_id=parent_id))

    def get_info(self,
                 configuration_id: int,
                 as_xml: Optional[bool] = False) -> Union[dict, str]:
        """
        Get full configuration info.

        Args:
            configuration_id (int): configuration identifier.

        Returns:
            Union[str, dict]: configuration content.
        """
        def callback(response: str) -> Union[dict, str]:
            if as_xml:
                return response

            root = xmltodict.parse(response)
            return root['com.pmease.quickbuild.model.Configuration']

        return self.quickbuild._request(
            'GET',
            'configurations/{}'.format(configuration_id),
            callback
        )
