from typing import List, Union

from quickbuild.helpers import response2py


class Agents:

    def __init__(self, quickbuild):
        self.quickbuild = quickbuild

    def get_active(self) -> Union[List[dict], str]:
        """
        Get list of active build agents.

        Returns:
            List[dict]: list of active build agents.
        """
        return self.quickbuild._request(
            'GET',
            'buildagents/active',
            callback=response2py,
        )

    def get_inactive(self) -> Union[List[dict], str]:
        """
        Get list of inactive build agents.

        Returns:
            List[dict]: list of inactive build agents.
        """
        return self.quickbuild._request(
            'GET',
            'buildagents/inactive',
            callback=response2py,
        )

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

    def get_running_steps(self, node_address: str) -> Union[List[dict], str]:
        """
        Get list of running steps on specified build agent (since 5.1.24).

        Returns:
            List[dict]: list of running steps.
        """
        return self.quickbuild._request(
            'GET',
            'buildagents/{}/running_steps'.format(node_address),
            callback=response2py,
        )
