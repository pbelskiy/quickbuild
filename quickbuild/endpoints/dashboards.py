from functools import partial
from typing import List, Optional, Union

from quickbuild.helpers import ContentType, response2py


class Dashboards:

    def __init__(self, quickbuild):
        self.quickbuild = quickbuild

    def get(self) -> List[dict]:
        """
        Get all dashboards in the system.

        Returns:
            List[dict]: list of all dashboards.
        """
        return self.quickbuild._request(
            'GET',
            'dashboards',
            callback=response2py,
        )

    def get_info(self,
                 dashboard_id: int,
                 *,
                 content_type: Optional[ContentType] = None
                 ) -> Union[dict, str]:
        """
        Get information about specified dashboard.

        Args:
            dashboard_id (int):
                Dashboard identifier.

            content_type (Optional[ContentType]):
                Select needed content type, if not set default value of client
                instance is used.

        Returns:
            Union[dict, str]: dashboard detailed information.
        """
        return self.quickbuild._request(
            'GET',
            'dashboards/{}'.format(dashboard_id),
            callback=partial(response2py, content_type=content_type),
            content_type=content_type,
        )
