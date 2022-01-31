from quickbuild.helpers import response2py


class Nodes:
    """
    Interact with attributes of grid node.

    https://wiki.pmease.com/display/QB10/Get+and+Set+User+Attributes+of+Grid+Node
    https://wiki.pmease.com/display/QB10/Get+System+Attributes+of+Grid+Node
    """
    def __init__(self, quickbuild):
        self.quickbuild = quickbuild

    def get_system_attributes(self, name: str) -> dict:
        """
        Get system attributes of grid node.

        This feature is available since QuickBuild 5.1.22

        Returns:
            dict: attributes
        """
        return self.quickbuild._request(
            'GET',
            'system_attributes/{}'.format(name),
            callback=response2py,
        )
