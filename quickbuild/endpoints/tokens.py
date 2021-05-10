from typing import Dict, List, Optional

from quickbuild.helpers import response2py


class Tokens:
    """
    By operating tokens, one can authorize/unauthorize agents, or access agent
    details including token value and latest usage information.
    """
    def __init__(self, quickbuild):
        self.quickbuild = quickbuild

    def get(self, agent_address: Optional[str] = None) -> List[dict]:
        """
        Get token value and latest used information of agents.

        Args:
            agent_address (Optional[str]):
                Build agent address, eg. my-agent:8811. If param address is set
                to None, details of all agents will be returned.

        Returns:
            List[dict]: List of token and agent details
        """
        params = dict()  # type: Dict[str, str]

        if agent_address:
            params['address'] = agent_address

        return self.quickbuild._request(
            'GET',
            'tokens',
            callback=response2py,
            params=params,
        )

    def authorize(self, agent_ip: str, agent_port: Optional[int] = 8811) -> str:
        """
        Authorize a build agent to join the build grid.

        Args:
            agent_ip (str):
                The build agent IP address.

            agent_port (Optional[int]):
                The build agent port (default: 8811).

        Returns:
            str: identifier of the newly created token for the build agent
        """
        response = self.quickbuild._request(
            'GET',
            'tokens/authorize',
            params=dict(ip=agent_ip, port=agent_port),
        )

        return response

    def unauthorize(self, agent_ip: str, agent_port: Optional[int] = 8811) -> str:
        """
        Unauthorize an already authorized build agent.

        Args:
            agent_ip (str):
                The build agent IP address.

            agent_port (Optional[int]):
                The build agent port (default: 8811).

        Returns:
            str: identifier of the removed token representing the build agent.
        """
        response = self.quickbuild._request(
            'GET',
            'tokens/unauthorize',
            params=dict(ip=agent_ip, port=agent_port),
        )

        return response
