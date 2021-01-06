class Builds:

    def __init__(self, quickbuild):
        self.quickbuild = quickbuild

    def get_info(self, build_id: int) -> str:
        """
        Get build info as raw XML string.

        Args:
            build_id (int): build id.

        Returns:
            str: XML string.
        """
        return self.quickbuild._request('GET', 'builds/{}'.format(build_id))

    def get_status(self, build_id: int) -> str:
        """
        Get build status.

        Args:
            build_id (int): build id.

        Returns:
            str: Build status, for example: `SUCCESS`
        """
        return self.quickbuild._request('GET', 'builds/{}/status'.format(build_id))
