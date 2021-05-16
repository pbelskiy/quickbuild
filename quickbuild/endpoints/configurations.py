import datetime

from typing import List, Optional, Union

from quickbuild.helpers import response2py


class Configurations:

    def __init__(self, quickbuild):
        self.quickbuild = quickbuild

    def _get(self, params: dict) -> List[dict]:
        return self.quickbuild._request(
            'GET',
            'configurations',
            callback=response2py,
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
                 *,
                 as_xml: Optional[bool] = False
                 ) -> Union[dict, str]:
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

            return response2py(response)

        return self.quickbuild._request(
            'GET',
            'configurations/{}'.format(configuration_id),
            callback=callback
        )

    def get_path(self, configuration_id: int) -> str:
        """
        Get configuration path.

        Args:
            configuration_id (int): configuration identifier.

        Returns:
            str: configuration path.
        """
        return self.quickbuild._request(
            'GET',
            'configurations/{}/path'.format(configuration_id),
        )

    def get_name(self, configuration_id: int) -> str:
        """
        Get configuration name.

        Args:
            configuration_id (int): configuration identifier.

        Returns:
            str: configuration name.
        """
        return self.quickbuild._request(
            'GET',
            'configurations/{}/name'.format(configuration_id),
        )

    def get_description(self, configuration_id: int) -> str:
        """
        Get configuration description.

        Args:
            configuration_id (int): configuration identifier.

        Returns:
            str: configuration description.
        """
        return self.quickbuild._request(
            'GET',
            'configurations/{}/description'.format(configuration_id),
        )

    def get_error_message(self, configuration_id: int) -> str:
        """
        Get configuration error message.

        Args:
            configuration_id (int): configuration identifier.

        Returns:
            str: configuration error message.
        """
        return self.quickbuild._request(
            'GET',
            'configurations/{}/error_message'.format(configuration_id),
        )

    def get_run_mode(self, configuration_id: int) -> str:
        """
        Get configuration run mode.

        Args:
            configuration_id (int): configuration identifier.

        Returns:
            str: configuration run mode.
        """
        return self.quickbuild._request(
            'GET',
            'configurations/{}/run_mode'.format(configuration_id),
        )

    def get_schedule(self, configuration_id: int) -> dict:
        """
        Get configuration schedule.

        Args:
            configuration_id (int): configuration identifier.

        Returns:
            dict: configuration schedule.

        Raises:
            QBProcessingError: will be raised if schedule is inherited from
                               parent configuration.
        """
        return self.quickbuild._request(
            'GET',
            'configurations/{}/schedule'.format(configuration_id),
            callback=response2py,
        )

    def get_average_duration(self,
                             configuration_id: int,
                             *,
                             from_date: Optional[datetime.date],
                             to_date: Optional[datetime.date]
                             ) -> int:
        """
        Get configuration average duration.

        Args:
            configuration_id (int): configuration identifier.

        Returns:
            int: milliseconds of average build duration.
        """
        params = dict()

        if from_date:
            params['from_date'] = str(from_date)

        if to_date:
            params['to_date'] = str(to_date)

        return self.quickbuild._request(
            'GET',
            'configurations/{}/average_duration'.format(configuration_id),
            callback=response2py,
            params=params,
        )

    def get_success_rate(self,
                         configuration_id: int,
                         *,
                         from_date: Optional[datetime.date],
                         to_date: Optional[datetime.date]
                         ) -> int:
        """
        Get configuration success rate.

        Args:
            configuration_id (int): configuration identifier.

        Returns:
            int: value in the range of 0~100, with 0 stands for 0%, and 100
                 stands for 100%.
        """
        params = dict()

        if from_date:
            params['from_date'] = str(from_date)

        if to_date:
            params['to_date'] = str(to_date)

        return self.quickbuild._request(
            'GET',
            'configurations/{}/success_rate'.format(configuration_id),
            callback=response2py,
            params=params,
        )

    def get_parent(self, configuration_id: int) -> int:
        """
        Get parent configuration id.

        Args:
            configuration_id (int): configuration identifier.

        Returns:
            int: id of parent configuration.

        Raises:
            QBProcessingError: the configuration is root configuration and does
                               not have parent.
        """
        return self.quickbuild._request(
            'GET',
            'configurations/{}/parent'.format(configuration_id),
            callback=response2py,
        )
