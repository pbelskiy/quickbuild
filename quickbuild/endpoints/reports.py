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


class Reports:
    """
    https://wiki.pmease.com/display/QB10/Interact+with+Reports
    """
    def __init__(self, quickbuild):
        self.quickbuild = quickbuild

    def get_tracker(self, name: str) -> Tracker:
        """
        Here, tracker is the type of your reports tracker in QuickBuild:

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
