from typing import List, Union

from quickbuild.helpers import response2py


class Agents:

    def __init__(self, quickbuild):
        self.quickbuild = quickbuild

    def get_unauthorized(self) -> Union[List[dict], str]:
        """
        Get list of unauthorized build agents.

        Returns:
            List[dict]: list of unauthorized build agents.
        """
        return self.quickbuild._request(
            'GET',
            'buildagents/unauthorized',
            callback=response2py,
        )
