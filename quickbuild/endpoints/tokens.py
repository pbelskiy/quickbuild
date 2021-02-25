from typing import List, Optional

import xmltodict


class Tokens:

    def __init__(self, quickbuild):
        self.quickbuild = quickbuild

    def get(self, agent_address: Optional[str] = None) -> List[dict]:
        """
        Get token value and latest used information of agents.

        Args:
            agent_address (Optional[str]):
                Build agent address, eg. my-agent:8811.
                If param address is set to None, details of all agents will be returned.

        Returns:
            List[dict]: List of token and agent details
        """
        def callback(response: str) -> List[dict]:
            root = xmltodict.parse(response)

            tokens = []
            if root['list'] is not None:
                tokens = root['list']['com.pmease.quickbuild.model.Token']
                if isinstance(tokens, list) is False:
                    tokens = [tokens]
            return tokens

        params_agent_address = dict(address=agent_address) if agent_address else {}

        return self.quickbuild._request(
            'GET',
            'tokens',
            callback,
            params=params_agent_address,
        )

    def authorize(self, agent_ip: str, agent_port: int = 8811) -> str:
        """
        Authorize a build agent to join the build grid.

        Args:
            agent_ip (str): The build agent IP address.
            agent_port (int): The build agent port (default: 8811).

        Returns:
            str: identifier of the newly created token for the build agent
        """
        response = self.quickbuild._request(
            'GET',
            'tokens/authorize',
            params=dict(ip=agent_ip, port=agent_port),
        )

        return response

    def unauthorize(self, agent_ip: str, agent_port: int = 8811) -> str:
        """
        Unauthorize an already authorized build agent.

        Args:
            agent_ip (str): The build agent IP address.
            agent_port (int): The build agent port (default: 8811).

        Returns:
            str: identifier of the removed token representing the build agent.
        """
        response = self.quickbuild._request(
            'GET',
            'tokens/unauthorize',
            params=dict(ip=agent_ip, port=agent_port),
        )

        return response
