from quickbuild.helpers import response2py


class Nodes:
    """
    Interact with attributes of grid node.

    https://wiki.pmease.com/display/QB10/Get+and+Set+User+Attributes+of+Grid+Node
    https://wiki.pmease.com/display/QB10/Get+System+Attributes+of+Grid+Node
    """
    def __init__(self, quickbuild) -> None:
        self.quickbuild = quickbuild

    def get_user_attributes(self, name: str) -> dict:
        """
        Get user attributes of grid node.

        .. note::
            This feature is available since QuickBuild 5.0.26

        Args:
            name (str):
                Node name.

        Returns:
            dict: attributes
        """
        return self.quickbuild._request(
            'GET',
            'user_attributes/{}'.format(name),
            callback=response2py,
        )

    def set_user_attributes(self, name: str, data: str) -> None:
        """
        Set user attributes of grid node.

        .. note::
            This feature is available since QuickBuild 5.0.26

        Args:
            name (str):
                Node name.

            group_id (int):
                Group identifier.

        Returns:
            None
        """
        return self.quickbuild._request(
            'POST',
            'user_attributes/{}'.format(name),
            callback=response2py,
            data=data,
        )

    def get_system_attributes(self, name: str) -> dict:
        """
        Get system attributes of grid node.

        .. note::
            This feature is available since QuickBuild 5.1.22

        Args:
            name (str):
                Node name.

        Returns:
            dict: attributes
        """
        return self.quickbuild._request(
            'GET',
            'system_attributes/{}'.format(name),
            callback=response2py,
        )
