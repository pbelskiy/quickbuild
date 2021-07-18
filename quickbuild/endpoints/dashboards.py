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

    def get_id_by_fqn(self, fqn: str) -> int:
        """
        Get dashboard id by dashboard fqn (fully qualified name).

        <dashboard fqn> is of the form <user id>.<dashboard name>.

        Args:
            fqn (str): fqn (fully qualified name).

        Returns:
            int: dashboard identifier.

        Raises:
            QBProcessingError: will be raised if resource is not found.
        """
        return self.quickbuild.identifiers.get_dashboard_id_by_dashboard_fqn(fqn)

    def update(self, configuration: str) -> int:
        """
        Update a dashboard using XML/JSON configuration.

        Normally you do not need to create the configuration from scratch, you
        may retrieve it representation of the dashboard using `get_info()`,
        modify certain parts and use it as new configuration.

        Args:
            configuration (str): XML/JSON document.

        Returns:
            int: dashboard id being updated.
        """
        return self.quickbuild._request(
            'POST',
            'dashboards',
            callback=response2py,
            data=configuration
        )

    def create(self, configuration: str) -> int:
        """
        Create a dashboard using XML/JSON configuration.

        Please note that the posted configuration should NOT contain the id
        element; otherwise, QuickBuild will treat the post as an updating to the
        dashboard with that id.

        Normally you do not need to create the configuration from scratch, you
        may retrieve it representation of the dashboard using `get_info()`,
        modify certain parts and use it as new configuration.

        Args:
            configuration (str): XML/JSON document.

        Returns:
            int: dashboard id being created.

        Raises:
            QBError: configuration validation error
        """
        self.quickbuild._validate_for_id(configuration)

        return self.quickbuild._request(
            'POST',
            'dashboards',
            callback=response2py,
            data=configuration
        )

    def delete(self, dashboard_id: int) -> None:
        """
        Delete specified dashboard.

        Args:
            dashboard_id (int): dashboard identifier.

        Returns:
            int: dashboard id being deleted.
        """
        return self.quickbuild._request(
            'DELETE',
            'dashboards/{}'.format(dashboard_id),
            callback=response2py,
        )
