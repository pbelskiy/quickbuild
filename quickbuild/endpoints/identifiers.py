from quickbuild.helpers import response2py


class Identifiers:

    def __init__(self, quickbuild):
        self.quickbuild = quickbuild

    def get_configuration_id_by_path(self, path: str) -> int:
        """
        Get configuration id by path.

        Args:
            path (str): configuration path.

        Returns:
            int: configuration identifier.
        """
        params = dict(
            configuration_path=path
        )

        return self.quickbuild._request(
            'GET',
            'ids',
            callback=response2py,
            params=params,
        )
