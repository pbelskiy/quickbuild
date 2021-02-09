from typing import Dict, List, Optional, Union

import xmltodict


class Audits:

    def __init__(self, quickbuild):
        self.quickbuild = quickbuild

    def get(self,
            count: int,
            *,
            username: Optional[str] = None,
            source: Optional[str] = None,
            action: Optional[str] = None,
            since: Optional[str] = None,
            until: Optional[str] = None,
            first: Optional[int] = None
            ) -> List[dict]:
        """
        Get all users in the system.

        Args:
            count (int):
                Specified number of audit entries to return. This param must be
                specified in order not to mistakenly return all audits to stress
                the system.

            username (Optional[str]):
                Name of the user to audit. If not specified, audit log of all
                users will be searched.

            source (Optional[str]):
                Specify source of audit to match. The character * can be used in
                the source string to do wildcard match. If not specified, audits
                from all sources will be matched.

            action (Optional[str]):
                Action of the audit to match. If left empty, any action will be
                matched.

            since (Optional[str]):
                In the format of yyyy-MM-dd HH:mm, for example: 2009-11-12 13:00.
                If specified, search audits generated after this date.

            until (Optional[str]):
                In the format of yyyy-MM-dd HH:mm, for example: 2009-11-12 14:00.
                If specified, search builds generated before this date.

            first (Optional[int]):
                Specified first audit entry to return. If not specified, value
                0 is assumed.

        Returns:
            List[dict]: list of audits.
        """
        def callback(response: str) -> List[dict]:
            root = xmltodict.parse(response)
            users = root['list']['com.pmease.quickbuild.model.Audit']
            if isinstance(users, list):
                return users

            return [users]

        params = dict(count=count)  # type: Dict[str, Union[str, int]]

        if username:
            params['username'] = username

        if source:
            params['source'] = source

        if action:
            params['action'] = action

        if since:
            params['since'] = since

        if until:
            params['until'] = until

        if first:
            params['first'] = first

        return self.quickbuild._request(
            'GET',
            'audits',
            callback,
            params=params,
        )

    def count(self) -> int:
        """
        Get count of audits.

        Returns:
            int: count of audits.
        """
        def callback(response: str) -> int:
            return int(response)

        return self.quickbuild._request(
            'GET',
            'audits/count',
            callback,
        )
