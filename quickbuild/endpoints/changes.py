from typing import Any, Dict, Optional

from quickbuild.helpers import response2py


class Changes:

    def __init__(self, quickbuild):
        self.quickbuild = quickbuild

    def get_version(self) -> str:
        """
        Get the data version of changes.

        Returns:
            str: changes version.
        """
        return self.quickbuild._request('GET', 'changes/version')

    def get_commit_stats(self,
                         configuration: str,
                         *,
                         build: Optional[int] = None,
                         from_build: Optional[int] = None,
                         to_build: Optional[int] = None,
                         from_date: Optional[str] = None,
                         to_date: Optional[str] = None,
                         date_pattern: Optional[str] = None,
                         repository: Optional[str] = None,
                         committer: Optional[str] = None
                         ) -> dict:
        """
        Get the commit stats

        Args:
            configuration (str):
                Specify the configuration. By default, specify configuration id
                here, also, you can specify the configuration path directly.

            build (Optional[int]):
                Specify the build id you want.

            from_build (Optional[int]):
                Specify the from build when finding changes in a build range.

            to_build (Optional[int]):
                Specify the to build when finding changes in a build range.

            from_date (Optional[str]):
                Specify the from date when finding changes in a build range.

            to_date (Optional[str]):
                Specify the to date when finding changes in a build range.

            date_pattern (Optional[str]):
                Specify the date pattern when query by a date range, by default
                the pattern is `yyyyMMdd`. Valid date pattern can be found here

                https://docs.oracle.com/javase/1.5.0/docs/api/java/text/SimpleDateFormat.html

            repository (Optional[str]):
                Get the changes only in a specific repository.

            committer (Optional[str]):
                Get the changes only committed by a specified committer

        Returns:
            dict: commit stats
        """
        params = dict()  # type: Dict[str, Any]

        if build:
            params['build'] = build

        if from_build:
            params['from_build'] = from_build

        if to_build:
            params['to_build'] = to_build

        if from_date:
            params['from_date'] = from_date

        if to_date:
            params['to_date'] = to_date

        if date_pattern:
            params['date_pattern'] = date_pattern

        if repository:
            params['repository'] = repository

        if committer:
            params['committer'] = committer

        response = self.quickbuild._request(
            'GET',
            'changes/stats/{}'.format(configuration),
            callback=response2py,
            params=params,
        )

        return response
