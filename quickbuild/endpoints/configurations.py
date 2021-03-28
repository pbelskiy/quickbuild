from typing import List

import xmltodict


class Configurations:

    def __init__(self, quickbuild):
        self.quickbuild = quickbuild

    def get(self) -> List[dict]:
        """
        Get all configurations in the system. For performance reason, only
        brief  information of the configuration will be returned here, including
        `id`, `name`, `description`, `schedule`, `runMode`, `errorMessage`,
        `parent id`. You may get the full xml representation using id if necessary.

        Returns:
            List[dict]: list of configurations.
        """
        def callback(response: str) -> List[dict]:
            root = xmltodict.parse(response)
            configurations = root['list']['com.pmease.quickbuild.model.Configuration']
            if isinstance(configurations, list) is False:
                configurations = [configurations]
            return configurations

        return self.quickbuild._request(
            'GET',
            'configurations?recursive=true',
            callback
        )
