from datetime import datetime


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

    def get_begin_date(self, build_id: int) -> datetime:
        """
        Get build begin date.

        Args:
            build_id (int): build id.

        Returns:
            datetime: return datetime from stdlib.
        """
        def callback(response: str) -> datetime:
            return datetime.fromtimestamp(int(response) / 1000)

        response = self.quickbuild._request(
            'GET',
            'builds/{}/begin_date'.format(build_id),
            callback
        )

        return response
