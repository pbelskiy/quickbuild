from typing import List

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

    def get_categories(self) -> List[str]:
        """
        Get reports tracker categories.

        Returns:
            List[str]: categories list.
        """
        return self.quickbuild._request(
            'GET',
            '{}/reports'.format(self.name),
            callback=response2py,
        )

    def get_definition(self, name: str) -> dict:
        """
        Get the report definition (meta data).

        Args:
            name (str):
                Specify the report name from categories API.

        You may consider the report meta data as the schema of a table in
        database. Each report has an attribute group and in QuickBuild, the
        following groups are used:

        - BUILD
        - STATISTICS
        - HISTORY
        - AGGREGATION

        the group attribute tells QuickBuild where to find the report, for
        example, if a report belongs to BUILD group, then this report is
        stored in build related directory, otherwise, the report is stored in
        configuration related directory.

        Returns:
            dict: report definition.
        """
        return self.quickbuild._request(
            'GET',
            '{}/meta/{}'.format(self.name, name),
            callback=response2py,
        )


class Reports:
    """
    https://wiki.pmease.com/display/QB10/Interact+with+Reports
    """
    def __init__(self, quickbuild):
        self.quickbuild = quickbuild

    def get_tracker(self, name: str) -> Tracker:
        """
        Here, tracker is the type of your reports tracker in QuickBuild:

        Args:
            name (str): report tracker name, examples table below.

        Report Category	Name
        --------------- ----------
        Build Stats     buildstats
        SCM Changes     changes
        CheckStyle      checkstyle
        Cobertura       cobertura
        JaCoCo          jacoco
        CPD             cpd
        EMMA            emma
        FindBugs        findbugs
        Fxcop           fxcop
        JUnit           junit
        MBUnit          mbunit
        MSTest          mstest
        NCover          ncover
        NUnit           nunit
        PMD             pmd
        TestNG          testng
        Boost Test      boost

        Returns:
            Tracker: Tracker instance
        """
        return Tracker(self.quickbuild, name)
