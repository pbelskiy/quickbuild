from typing import List, Optional, Union

from quickbuild.helpers import response2py


class Measurements:

    def __init__(self, quickbuild):
        self.quickbuild = quickbuild

    def get(self,
            *,
            source: Optional[str] = None,
            period: Optional[str] = None,
            start_time: Optional[str] = None,
            end_time: Optional[str] = None,
            metric: Optional[str] = None,
            date_pattern: Optional[str] = None
            ) -> Union[List[dict], str]:
        """
        Get information about published files. Without any arguments server will
        return all measurements collected from all nodes in the last one hour.

        Args:
            source (Optional[str]):
                Specify the node you want to query. If not specified, then all
                nodes will be used. (Example: `myagent:8811`)

            period (Optional[str]):
                Specify the time range you want to query. by default, period is
                LAST_HOUR, this param can be one of: LAST_HOUR, LAST_2_HOURS,
                LAST_4_HOURS, LAST_DAY, LAST_WEEK, LAST_MONTH.

            start_time (Optional[str]):
                Specify the start time you want to query. If not specified,
                then an hour ago of to_date will be used.

            end_time (Optional[str]):
                Specify the end time you want to query. If not specified, then
                current time will be used.

            metric (Optional[str]):
                Specify the metric name you want to query. See below section
                for all available metric names. (Example: `disk.usage`)

                Available measurement metrics:
                https://wiki.pmease.com/display/QB10/Query+Grid+Measurements

            date_pattern (Optional[str]):
                Specify the date pattern you are using for from_date and to_date.
                By default, ISO 8601 is used.

        Returns:
            Union[List[dict], str]: list of measurements.
        """
        params = dict()

        if source:
            params['source'] = source

        if period:
            params['period'] = period

        if start_time:
            params['start_time'] = start_time

        if end_time:
            params['end_time'] = end_time

        if metric:
            params['metric'] = metric

        if date_pattern:
            params['date_pattern'] = date_pattern

        return self.quickbuild._request(
            'GET',
            'grid/measurements',
            callback=response2py,
            params=params,
        )

    def get_version(self) -> str:
        """
        Get current version for the measurements related REST API.

        Returns:
            str: measurements version.
        """
        return self.quickbuild._request(
            'GET',
            'grid/measurements/version',
        )
