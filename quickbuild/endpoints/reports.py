from typing import Any, Dict, List, Optional

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

        Args:
            name (str):
                Specify the report name from categories API.

        Returns:
            dict: report definition.
        """
        return self.quickbuild._request(
            'GET',
            '{}/meta/{}'.format(self.name, name),
            callback=response2py,
        )

    def get_aggregations(self,
                         report_group: str,
                         configuration_or_build_id: int
                         ) -> List[str]:
        """
        In QuickBuild, the report data are stored by report sets or by aggregations.
        The report set is specified in the publish step, and the aggregation name
        is specified in the aggregation definition.

        Args:
            report_group (str):
                The report group, can be one of the following:
                BUILD, STATISTICS, HISTORY, AGGREGATION.

            configuration_or_build_id (int):
                For BUILD group, the id should be a valid build id, otherwise,
                the configuration id should be specified.

        Returns:
            List[str]: aggregated report data.
        """
        return self.quickbuild._request(
            'GET',
            '{}/reportsets/{}/{}'.format(
                self.name,
                report_group,
                configuration_or_build_id,
            ),
            callback=response2py,
        )

    def get_build_stats(self, build_id: int, reportset: str) -> dict:
        """
        Get the build stats.

        Args:
            build_id (int):
                Specify the build id.

            reportset (str):
                The report set you want.

        Returns:
            dict: get build stats.
        """
        return self.quickbuild._request(
            'GET',
            '{}/buildstats/{}/{}'.format(self.name, build_id, reportset),
            callback=response2py,
        )

    def get_records_size(self,
                         report_name: str,
                         configuration_or_build_id: int,
                         reportset: str,
                         filters: Optional[str] = None
                         ) -> int:
        """
        Get number of total records

        Args:
            report_name (str):
                Specify the report name.

            configuration_or_build_id (int):
                According to the report you specified, supply a valid build id
                when report belongs to BUILD group, otherwise, configuration id
                is needed.

            reportset (str):
                Specify the report set or aggregation name.

            filters (Optional[str]):
                Specify filters based on SQL to filter the records, for example,
                duration>5 and duration<10, the fields available can be found in
                the report meta data definition.

                Example: "(status='ERROR') or (status='FAILURE')"

        Returns:
            int: number of total records.
        """
        params = dict()

        if filters:
            params['filters'] = filters

        return self.quickbuild._request(
            'GET',
            '{}/size/{}/{}/{}'.format(
                self.name,
                report_name,
                configuration_or_build_id,
                reportset,
            ),
            params=params,
            callback=response2py,
        )

    def get_records_data(self,
                         report_name: str,
                         configuration_or_build_id: int,
                         reportset: str,
                         *,
                         offset: Optional[int] = None,
                         limit: Optional[int] = None,
                         filters: Optional[str] = None
                         ) -> int:  # pylint: disable=too-many-arguments.
        """
        Get the report records by page.

        Args:
            report_name (str):
                Specify the report name.

            configuration_or_build_id (int):
                According to the report you specified, the id is a build id when
                report belongs to BUILD group, otherwise, configuration id is
                needed.

            reportset (str):
                The report set or aggregation name

            offset (Optional[int]):
                The first record you want to retrieve. By default, the offset
                is 0, i.e., from the first record.

            limit (Optional[int]):
                The number of records you want to retrieve. By default, the
                number of limit is 50.

            filters (Optional[str]):
                Specify filters based on SQL to filter the records, for example,
                duration>5 and duration<10, the fields available can be found in
                the report meta data definition.

        Returns:
            int: number of total records.
        """
        params = dict()  # type: Dict[str, Any]

        if offset:
            params['offset'] = offset

        if limit:
            params['limit'] = limit

        if filters:
            params['filters'] = filters

        return self.quickbuild._request(
            'GET',
            '{}/records/{}/{}/{}'.format(
                self.name,
                report_name,
                configuration_or_build_id,
                reportset,
            ),
            params=params,
            callback=response2py,
        )


class Reports:
    """
    https://wiki.pmease.com/display/QB10/Interact+with+Reports
    """
    def __init__(self, quickbuild) -> None:
        self.quickbuild = quickbuild

    def get_tracker(self, name: str) -> Tracker:
        """
        Here, tracker is the type of your reports tracker in QuickBuild:

        Args:
            name (str): report tracker name, examples table below.

        +------------------+-------------+
        | Report category  | Name        |
        +==================+=============+
        | Build Stats      | buildstats  |
        +------------------+-------------+
        | SCM Changes      | changes     |
        +------------------+-------------+
        | CheckStyle       | checkstyle  |
        +------------------+-------------+
        | Cobertura        | cobertura   |
        +------------------+-------------+
        | JaCoCo           | jacoco      |
        +------------------+-------------+
        | CPD              | cpd         |
        +------------------+-------------+
        | EMMA             | emma        |
        +------------------+-------------+
        | FindBugs         | findbugs    |
        +------------------+-------------+
        | Fxcop            | fxcop       |
        +------------------+-------------+
        | JUnit            | junit       |
        +------------------+-------------+
        | MBUnit           | mbunit      |
        +------------------+-------------+
        | MSTest           | mstest      |
        +------------------+-------------+
        | NCover           | ncover      |
        +------------------+-------------+
        | NUnit            | nunit       |
        +------------------+-------------+
        | PMD              | pmd         |
        +------------------+-------------+
        | TestNG           | testng      |
        +------------------+-------------+
        | Boost Test       | boost       |
        +------------------+-------------+

        Returns:
            Tracker: Tracker instance
        """
        return Tracker(self.quickbuild, name)
