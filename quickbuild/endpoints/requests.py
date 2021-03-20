from typing import Dict, List, Optional

import xmltodict


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
        def callback(response: str) -> List[dict]:
            root = xmltodict.parse(response)
            requests = root['list']['com.pmease.quickbuild.BuildRequest']
            if isinstance(requests, list) is False:
                requests = [requests]
            return requests

        params = dict()  # type: Dict[str, int]

        if configuration_id:
            params['configuration_id'] = configuration_id

        if trigger_user_id:
            params['trigger_user_id'] = trigger_user_id

        return self.quickbuild._request(
            'GET',
            'build_requests',
            callback,
            params=params
        )
