from typing import Any, Dict, List, Optional

from quickbuild.helpers import response2py


class Changes:
    """
    https://wiki.pmease.com/display/QB10/Interact+with+Changes

    Data structure of the changes:

    In QuickBuild, we use Changeset and Modification to represent a SCM commit.
    A changeset is an atomic collection of changes to files in a repository and
    it usually contains several modifications. A modification means developer
    made a specific action to a file when committed to a repository.

    In QuickBuild, the actions include:
    * ADD
    * MODIFY
    * DELETE

    The action in some SCM, for example, git, mercurial, have more actions, like
    rename, in QuickBuild, it will be speared into two actions, i.e. DELETE first,
    and then ADD, and maybe there are also other actions, QuickBuild will use
    MODIFY action to represent.
    """
    def __init__(self, quickbuild) -> None:
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

    def get_changesets(self,
                       configuration: str,
                       *,
                       build: Optional[int] = None,
                       from_build: Optional[int] = None,
                       to_build: Optional[int] = None,
                       date_pattern: Optional[str] = None,
                       from_date: Optional[str] = None,
                       to_date: Optional[str] = None,
                       repository: Optional[int] = None,
                       committer: Optional[int] = None,
                       offset: Optional[int] = None,
                       limit: Optional[int] = None,
                       asc: Optional[bool] = None
                       ) -> List[dict]:
        """
        Get changesets.

        Args:
            configuration (str):
                Specify the configuration. By default, specify configuration id
                here, also, you can specify the configuration path directly.

            build (Optional[int]):
                Specify the build id you want.

            from_build (Optional[int]):
                Specify the from build when finding changes in a build range,
                must be specified with to_build.

            to_build (Optional[int]):
                Specify the to build when finding changes in a build range,
                must be specified with from_build.

            date_pattern (Optional[str]):
                Specify the date pattern when query by a date range, by default
                the pattern is `yyyyMMdd`. Valid date pattern can be found here

                https://docs.oracle.com/javase/1.5.0/docs/api/java/text/SimpleDateFormat.html

            from_date (Optional[str]):
                Specify the from date when finding changes in a build range.

            to_date (Optional[str]):
                Specify the to date when finding changes in a build range.

            repository (Optional[int]):
                Get the changes only in a specific repository.

            committer (Optional[int]):
                Get the changes only committed by the specified committer.

            offset (Optional[int]):
                Specify the first record when iterate the records, by default,
                the offset is 0.

            limit (Optional[int]):
                Specify the number of total records you want to retrieve, by
                default, the limit is 50.

            asc (Optional[bool]):
                Boolean type, specify the order by commit date ascendent or
                descendent, by default, it is descendent.

        Returns:
            List[dict]: changesets list.
        """
        params = dict()  # type: Dict[str, Any]

        if build:
            params['build'] = build

        if from_build:
            params['from_build'] = from_build

        if to_build:
            params['to_build'] = to_build

        if date_pattern:
            params['date_pattern'] = date_pattern

        if from_date:
            params['from_date'] = from_date

        if to_date:
            params['to_date'] = to_date

        if repository:
            params['repository'] = repository

        if committer:
            params['committer'] = committer

        if offset:
            params['offset'] = offset

        if limit:
            params['limit'] = limit

        if asc:
            params['asc'] = asc

        response = self.quickbuild._request(
            'GET',
            'changes/{}'.format(configuration),
            callback=response2py,
            params=params,
        )

        return response

    def get_build_commits_changesets(self, build_id: int) -> List[dict]:
        """
        Get the changesets of the build_id lively.

        Most of the aforementioned APIs are only
        callable when build finish. Sometimes, you may want to query the
        changesets during the build is still running.

        Args:
            build_id (int):
                Build id.

        Returns:
            List[dict]: changesets list.
        """
        response = self.quickbuild._request(
            'GET',
            'changes/commits/build/{}'.format(build_id),
            callback=response2py,
        )

        return response

    def get_build_stats_changesets(self, build_id: int) -> List[dict]:
        """
        Get the stats of the changesets of the build_id lively.

        Most of the aforementioned APIs are only
        callable when build finish. Sometimes, you may want to query the
        changesets during the build is still running.

        Args:
            build_id (int):
                Build id.

        Returns:
            List[dict]: changesets list.
        """
        response = self.quickbuild._request(
            'GET',
            'changes/stats/build/{}'.format(build_id),
            callback=response2py,
        )

        return response
