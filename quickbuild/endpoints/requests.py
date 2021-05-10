from typing import Dict, List, Optional

from quickbuild.helpers import response2py


class Requests:
    """
    Build request object can be used to request new build or cancel running build.
    """
    def __init__(self, quickbuild):
        self.quickbuild = quickbuild

    def get(self,
            *,
            configuration_id: Optional[int] = None,
            trigger_user_id: Optional[int] = None
            ) -> List[dict]:
        """
        Get build info as raw XML string.

        Args:
            configuration_id (Optional[int]):
                Identifier of a configuration to filter on, if missing, QB will
                return all build requests in the system.

            trigger_user_id (Optional[int]):
                Identifier of the user triggering the request to filter on, if
                this param is missing, QB will return build requests triggered
                by all users in the system.

        Returns:
            List[dict]: list of build requests.
        """
        params = dict()  # type: Dict[str, int]

        if configuration_id:
            params['configuration_id'] = configuration_id

        if trigger_user_id:
            params['trigger_user_id'] = trigger_user_id

        return self.quickbuild._request(
            'GET',
            'build_requests',
            callback=response2py,
            params=params
        )

    def create(self, configuration: str) -> dict:
        """
        New build can be requested by posting XML representation of the build
        request object.

        Args:
            configuration (str):
                XML of build request object.

        Returns:
            dict: content is XML representation of request result including the
            generated build request id.

        Raises:
            QBProcessingError: will be raised if the request is aggregated.
        """
        return self.quickbuild._request(
            'POST',
            'build_requests',
            callback=response2py,
            data=configuration,
        )

    def trigger(self, configuration_id: int) -> dict:
        """
        Since QuickBuild 6.0.14, one can also trigger new build.

        Args:
            configuration_id (int):
                Identifier of a configuration.

        Returns:
            dict: content is XML representation of request result including the
            generated build request id.

        Raises:
            QBProcessingError: will be raised if the request is aggregated.
        """
        return self.quickbuild._request(
            'GET',
            'trigger',
            callback=response2py,
            params=dict(configuration_id=configuration_id)
        )

    def delete(self, request_id: str) -> None:
        """
        Delete existing build request. If the build associated with the build
        request is already running, it will be forcibly stopped.

        Args:
            request_id (str):
                Identifier of a build request.
        """
        return self.quickbuild._request(
            'DELETE',
            'build_requests/{}'.format(request_id),
        )
