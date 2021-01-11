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

    def get_version(self, build_id: int) -> str:
        """
        Get build version.

        Args:
            build_id (int): build id.

        Returns:
            str: build version
        """
        return self.quickbuild._request('GET', 'builds/{}/version'.format(build_id))

    def get_duration(self, build_id: int) -> int:
        """
        Get build duration in ms. QBProcessingError will be raised if build is not finished.

        Args:
            build_id (int): build id.

        Returns:
            int: build duration in ms
        """
        def callback(response: str) -> int:
            return int(response)

        response = self.quickbuild._request(
            'GET',
            'builds/{}/duration'.format(build_id),
            callback
        )

        return response

    def get_request_id(self, build_id: int) -> str:
        """
        Get request id. QBProcessingError will be raised if build is finished.

        Args:
            build_id (int): build id.

        Returns:
            str: request id. Example: fd2339a1-bc71-429d-b4ee-0ac650c342fe
        """

        response = self.quickbuild._request(
            'GET',
            'builds/{}/request_id'.format(build_id)
        )

        return response
