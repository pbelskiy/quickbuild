from typing import List

import xmltodict


class Tokens:
    """With tokens, one can authorize/unauthorize agents, or access agent
    details including token value and latest usage information.
    """

    def __init__(self, quickbuild):
        self.quickbuild = quickbuild

    def authorize(self, agent_ip: str, agent_port: int = 8811) -> str:
        """
        Authorize a build agent to join the build grid.

        Args:
            agent_ip (str): The build agent IP address.
            agent_port (int): The build agent port.

        Returns:
            str: identifier of the newly created token for the build agent
        """
        response = self.quickbuild._request(
            'GET',
            'tokens/authorize?ip={}&port={}'.format(agent_ip, agent_port)
        )

        return response

    def unauthorize(self, agent_ip: str, agent_port: int = 8811) -> str:
        """
        Unauthorize an already authorized build agent.

        Args:
            agent_ip (str): The build agent IP address.
            agent_port (int): The build agent port.

        Returns:
            str: identifier of the removed token representing the build agent.
        """
        response = self.quickbuild._request(
            'GET',
            'tokens/unauthorize?ip={}&port={}'.format(agent_ip, agent_port)
        )

        return response

    def get_token_and_agent_details(self, agent_address: str) -> List[dict]:
        """
        Get token value and latest used information of agents.

        Args:
            agent_address (str): Build agent address, eg. my-agent:8811.
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

        agent_address_query_string = '?address={}'.format(agent_address) if agent_address else ''

        return self.quickbuild._request(
            'GET',
            'tokens{}'.format(agent_address_query_string),
            callback
        )