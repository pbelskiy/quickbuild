from functools import partial
from typing import List, Optional, Union

from quickbuild.helpers import response2py


class Memberships:

    def __init__(self, quickbuild):
        self.quickbuild = quickbuild

    def get(self) -> List[dict]:
        """
        Get all memberships in the system.

        Returns:
            List[dict]: list of all memberships.
        """
        return self.quickbuild._request(
            'GET',
            'memberships',
            callback=response2py,
        )

    def get_info(self,
                 membership_id: int,
                 *,
                 as_xml: Optional[bool] = False
                 ) -> Union[dict, str]:
        """
        Get full membership info.

        Args:
            membership_id (int): membership identifier.

        Returns:
            Union[str, dict]: membership content.
        """
        return self.quickbuild._request(
            'GET',
            'memberships/{}'.format(membership_id),
            callback=partial(response2py, as_xml=as_xml)
        )
