from typing import List, Optional, Union

from quickbuild.helpers import response2py


class Tracker:

    def __init__(self, quickbuild, name: str) -> None:
        self.quickbuild = quickbuild
        self.name = name

    def get_version(self) -> str:
        """
        Get tracker version.

        Returns:
            str: tracker version
        """
        return self.quickbuild._request(
            'GET',
            '{}/version'.format(self.name)
        )

    def get_size(self,
                 configuration: Union[int, str],
                 *,
                 build: Optional[int] = None,
                 from_build: Optional[int] = None,
                 to_build: Optional[int] = None
                 ) -> int:
        """
        Retrieve the issues size related to a configuration.

        Args:
            configuration (str):
                Specify the configuration. By default, specify configuration id
                here, if you want to specify a configuration path, you need add
                prefix `PATH:`, for example: `PATH:root/My/DEV`.

                Since QB version 5.0.14: Specify the configuration path directly
                for example: `root/My/DEV`, no need `PATH:prefix` anymore.

            build (int):
                The id of a specific build.

            from_build (int):
                Specify the from build when finding changes in a build range.

            to_build (int):
                Specify the to build when finding changes in a build range.

        Returns:
            int: issues size
        """
        params = dict()

        if build:
            params['build'] = build

        if from_build:
            params['from_build'] = from_build

        if to_build:
            params['to_build'] = to_build

        return self.quickbuild._request(
            'GET',
            '{}/size/{}'.format(self.name, configuration),
            callback=response2py,
        )

    def get_issues(self,
                   configuration: Union[int, str],
                   *,
                   build: Optional[int] = None,
                   from_build: Optional[int] = None,
                   to_build: Optional[int] = None,
                   offset: Optional[int] = None,
                   limit: Optional[int] = None,
                   asc: Optional[bool] = None
                   ) -> List[dict]:
        """
        Retrieve the issues.

        Args:
            configuration (str):
                Specify the configuration. By default, specify configuration id
                here, if you want to specify a configuration path, you need add
                prefix `PATH:`, for example: `PATH:root/My/DEV`.

                Since QB version 5.0.14: Specify the configuration path directly
                for example: `root/My/DEV`, no need `PATH:prefix` anymore.

            build (Optional[int]):
                The id of a specific build.

            from_build (Optional[int]):
                Specify the from build when finding changes in a build range.

            to_build (Optional[int]):
                Specify the to build when finding changes in a build range.

            offset (Optional[int]):
                Specify the first record when iterate the records, by default,
                the offset is 0.

            limit (Optional[int]):
                Specify the total records you want to retrieve, by default,
                the limit is 50.

            asc (Optional[bool]):
                Specify order by issue key ascendent or descendent, by default,
                it is ascendent.

        Returns:
            List[dict]: issues list.
        """
        def callback(response: str) -> List[dict]:
            return response2py(response, self.quickbuild._content_type)['row']

        params = dict()

        if build:
            params['build'] = build

        if from_build:
            params['from_build'] = from_build

        if to_build:
            params['to_build'] = to_build

        if offset:
            params['offset'] = offset

        if limit:
            params['limit'] = limit

        if asc:
            params['asc'] = asc

        return self.quickbuild._request(
            'GET',
            '{}/issues/{}'.format(self.name, configuration),
            callback=callback,
        )

    def get_builds(self,
                   configuration: Union[int, str],
                   issuekey: str,
                   *,
                   count: Optional[int] = None
                   ) -> List[dict]:
        """
        Retrieve the builds of an issue.
        TODO: add support for QB  version < 5.0.14

        Args:
            configuration (str):
                Specify the configuration. By default, specify configuration id
                here, if you want to specify a configuration path, you need add
                prefix `PATH:`, for example, `PATH:root/My/DEV`.

            issuekey (str):
                The issue key you want to search.

            count (Optional[int]):
                Specify at most how many records you want. If not specified,
                all records found will return.

        Returns:
            List[dict]: issues list.
        """
        params = dict()

        if count:
            params['count'] = count

        return self.quickbuild._request(
            'GET',
            '{}/{}/builds/{}'.format(self.name, issuekey, configuration),
            callback=response2py,
        )

    def get_changes(self,
                    configuration: Union[int, str],
                    issuekey: str,
                    *,
                    count: Optional[int] = None
                    ) -> List[dict]:
        """
        Retrieve the changes of an issue.
        TODO: add support for QB  version < 5.0.14

        Args:
            configuration (str):
                Specify the configuration. By default, specify configuration
                id here. You can also specify the configuration path directly.

            issuekey (str):
                The issue key you want to search.

            count (Optional[int]):
                Specify at most how many records you want. If not specified,
                all records found will return.

        Returns:
            List[dict]: issues list.
        """
        params = dict()

        if count:
            params['count'] = count

        return self.quickbuild._request(
            'GET',
            '{}/{}/changes/{}'.format(self.name, issuekey, configuration),
            callback=response2py,
        )


class Issues:
    """
    https://wiki.pmease.com/display/QB10/Interact+with+Issues
    """
    def __init__(self, quickbuild):
        self.quickbuild = quickbuild

    def get_tracker(self, name: str) -> Tracker:
        """
        Since QuickBuild 4.0, you can retrieve issues via RESTful APIs.
        The base URI for changes RESTful APIs is: `/rest/{tracker}`

        Here, tracker is the type of your issue tracker in QuickBuild:

        - Jira - /rest/jira
        - Trac - /rest/trac
        - Bugzilla - /rest/bugzilla

        Returns:
            Tracker: Tracker instance
        """
        return Tracker(self.quickbuild, name)
