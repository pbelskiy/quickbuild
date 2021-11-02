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
            List[dict]: list of resources.
        """
        return Tracker(self.quickbuild, name)
