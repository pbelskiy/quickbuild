from typing import Optional

from quickbuild.helpers import response2py


class Tracker:

    def __init__(self, quickbuild, name: str):
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
                 configuration: str,
                 *,
                 build: Optional[int] = None,
                 from_build: Optional[int] = None,
                 to_build: Optional[int] = None
                 ) -> int:
        """
        Retrieve the issues size related to a configuration.

        Args:
            configuration (str):
                Specify the configuration. By default, specify configuration id here,
                if you want to specify a configuration path, you need add prefix PATH:,
                for example: `PATH:root/My/DEV`.

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


class Issues:

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
            List[dict]: list of resources
        """
        return Tracker(self.quickbuild, name)
