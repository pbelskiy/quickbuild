from datetime import datetime
from functools import partial
from typing import Dict, List, Optional, Union

from quickbuild.helpers import ContentType, response2py


class Builds:

    def __init__(self, quickbuild):
        self.quickbuild = quickbuild

    def get_info(self,
                 build_id: int,
                 *,
                 content_type: Optional[ContentType] = None
                 ) -> Union[dict, str]:
        """
        Get build info as raw XML string.

        Args:
            build_id (int): build id.

            content_type (Optional[ContentType]):
                Select needed content type if not set, default value of client
                instance is used.

        Returns:
            Union[dict, str]: build information.
        """
        return self.quickbuild._request(
            'GET',
            'builds/{}'.format(build_id),
            callback=partial(response2py, content_type=content_type),
            content_type=content_type,
        )

    def get_status(self, build_id: int) -> str:
        """
        Get build status.

        Args:
            build_id (int): build id.

        Returns:
            str: Build status, for example: `SUCCESS`
        """
        return self.quickbuild._request(
            'GET',
            'builds/{}/status'.format(build_id)
        )

    def get_begin_date(self, build_id: int) -> datetime:
        """
        Get build begin date.

        Args:
            build_id (int): build id.

        Returns:
            datetime: return datetime from stdlib.
        """
        def callback(response: str) -> datetime:
            return datetime.fromtimestamp(int(response) / 1000)

        response = self.quickbuild._request(
            'GET',
            'builds/{}/begin_date'.format(build_id),
            callback=callback
        )

        return response

    def get_version(self, build_id: int) -> str:
        """
        Get build version.

        Args:
            build_id (int): build id.

        Returns:
            str: build version
        """
        return self.quickbuild._request(
            'GET',
            'builds/{}/version'.format(build_id)
        )

    def get_duration(self, build_id: int) -> int:
        """
        Get build duration in ms. QBProcessingError will be raised if build is
        not finished.

        Args:
            build_id (int): build id.

        Returns:
            int: build duration in ms
        """
        def callback(response: str) -> int:
            return int(response)

        response = self.quickbuild._request(
            'GET',
            'builds/{}/duration'.format(build_id),
            callback=callback
        )

        return response

    def get_request_id(self, build_id: int) -> str:
        """
        Get request id. QBProcessingError will be raised if build is finished.

        Args:
            build_id (int): build id.

        Returns:
            str: request id. Example: fd2339a1-bc71-429d-b4ee-0ac650c342fe
        """
        response = self.quickbuild._request(
            'GET',
            'builds/{}/request_id'.format(build_id)
        )

        return response

    def get_id_by_request_id(self, identifier: int) -> int:
        """
        Get build id by request id.

        Args:
            identifier (int): request identifier.

        Returns:
            int: build identifier.

        Raises:
            QBProcessingError: will be raised if resource is not found.
        """
        return self.quickbuild.identifiers.get_build_id_by_request_id(identifier)

    def get_id_by_build_name(self, name: str) -> int:
        """
        Get build id by build name.

        For example how to get id of latest build in configuration with id 1,
        name will be `1.latest`

        Args:
            name (str): build name.

        Returns:
            int: build identifier.

        Raises:
            QBProcessingError: will be raised if resource is not found.
        """
        return self.quickbuild.identifiers.get_build_id_by_build_name(name)

    def get_steps(self, build_id: int) -> str:
        """
        Get build steps.

        Args:
            build_id (int): build id.

        Returns:
            str: builds steps as XML document
        """
        response = self.quickbuild._request(
            'GET',
            'builds/{}/steps'.format(build_id)
        )

        return response

    def get_repositories(self, build_id: int) -> str:
        """
        Get build repositories.

        Args:
            build_id (int): build id.

        Returns:
            str: builds repositories as XML document
        """
        response = self.quickbuild._request(
            'GET',
            'builds/{}/repositories'.format(build_id)
        )

        return response

    def get_dependencies(self, build_id: int) -> str:
        """
        Get build dependencies.

        Args:
            build_id (int): build id.

        Returns:
            str: builds dependencies as XML document
        """
        response = self.quickbuild._request(
            'GET',
            'builds/{}/dependencies'.format(build_id)
        )

        return response

    def get_dependents(self, build_id: int) -> str:
        """
        Get build dependents.

        Args:
            build_id (int): build id.

        Returns:
            str: builds dependents as XML document
        """
        response = self.quickbuild._request(
            'GET',
            'builds/{}/dependents'.format(build_id)
        )

        return response

    def get_files(self, build_id: int, path: str) -> str:
        """
        Get information about published files.

        Args:
            build_id (int):
                Build id.

            path (str):
                Represents the relative path under publish directory of the
                specified build.

        Returns:
            str: information about files and directories under the specified path.

        Raises:
            QBProcessingError: will be raised if specified path does not exist.
        """
        params = dict(
            build_id=build_id,
            path=path,
        )

        response = self.quickbuild._request(
            'GET',
            'files',
            callback=response2py,
            params=params,
        )

        return response

    def get_notifications(self,
                          last_notified_build_id: Optional[int] = None
                          ) -> Union[List[dict], str]:
        """
        Get notifications belonging to current user, specified when client
        instance was initialized.

        Args:
            last_notified_build_id (Optional[int]):
                If not specified, the most recent notification will be returned;
                otherwise, all notifications after specified build will be returned.

        Returns:
            Union[List[dict], str]: list of builds to be notified.
        """
        params = dict()

        if last_notified_build_id:
            params['last_notified_build_id'] = last_notified_build_id

        response = self.quickbuild._request(
            'GET',
            'notifications',
            callback=response2py,
            params=params,
        )

        return response

    def search(self,
               count: int,
               *,
               configuration_id: Optional[int] = None,
               recursive: Optional[bool] = False,
               from_date: Optional[str] = None,
               to_date: Optional[str] = None,
               version: Optional[str] = None,
               status: Optional[str] = None,
               user_id: Optional[int] = None,
               master_node: Optional[str] = None,
               promoted_from_id: Optional[int] = None,
               request_id: Optional[int] = None,
               first: Optional[int] = None
               ) -> List[dict]:
        """
        Search builds by criteria.

        Args:
            count (int):
                Specify number of builds to return. This parameter is required.

            configuration_id (Optional[int]):
                This tells QuickBuild under which configuration id to search builds.
                If not specified, all configurations will be searched.

            recursive (Optional[bool]):
                If set to true, QuickBuild will also search builds in all descendent
                configurations of specified configuration. The value is assumed as
                false if not specified.

            from_date (Optional[str]):
                In the format of yyyy-MM-dd, for example: 2009-11-12. If specified,
                search builds generated after this date.

            to_date (Optional[str]):
                In the format of yyyy-MM-dd, for example: 2009-11-12. If specified,
                search builds generated before this date.

            version (Optional[str]):
                Specify the build version to match. The character * can be used in
                the version string to do wildcard match. If not specified, all
                versions will be matched.

            status (Optional[str]):
                Status of the build to match. Valid build statuses are:
                SUCCESSFUL, FAILED, RECOMMENDED, CANCELLED, RUNNING, TIMEOUT.
                If left empty, any build status will be matched.

            user_id (Optional[int]):
                Match builds which is triggered by specified user.
                If not specified, builds triggered by any user will be matched.

            master_node (Optional[str]):
                Match builds with master step running on specified node if specified.

            promoted_from_id (Optional[int]):
                Match builds promoted from specified build id if specified.

            request_id (Optional[int]):
                If specified, match builds with specified build request id.

            first (Optional[int]):
                Specify start position of search results. Position 0 is assumed
                if this param is not specified.

        Returns:
            List[dict]: builds search result list.
        """
        params = dict(
            count=count,
        )  # type: Dict[str, Union[str, int, bool]]

        if configuration_id:
            params['configuration_id'] = configuration_id

        if recursive:
            params['recursive'] = recursive

        if from_date:
            params['from_date'] = from_date

        if to_date:
            params['to_date'] = to_date

        if version:
            params['version'] = version

        if status:
            params['status'] = status

        if user_id:
            params['user_id'] = user_id

        if master_node:
            params['master_node'] = master_node

        if promoted_from_id:
            params['promoted_from_id'] = promoted_from_id

        if request_id:
            params['request_id'] = request_id

        if first:
            params['first'] = first

        response = self.quickbuild._request(
            'GET',
            'builds',
            callback=response2py,
            params=params
        )

        return response

    def count(self,
              *,
              configuration_id: Optional[int] = None,
              recursive: Optional[bool] = False,
              from_date: Optional[str] = None,
              to_date: Optional[str] = None,
              version: Optional[str] = None,
              status: Optional[str] = None,
              user_id: Optional[int] = None,
              promoted_from_id: Optional[int] = None,
              request_id: Optional[int] = None
              ) -> int:
        """
        Get builds count by criteria.

        Args:
            configuration_id (Optional[int]):
                This tells QuickBuild under which configuration id to search builds.
                If not specified, all configurations will be searched.

            recursive (Optional[bool]):
                If set to true, QuickBuild will also search builds in all descendent
                configurations of specified configuration. The value is assumed as
                false if not specified.

            from_date (Optional[str]):
                In the format of yyyy-MM-dd, for example: 2009-11-12. If specified,
                search builds generated after this date.

            to_date (Optional[str]):
                In the format of yyyy-MM-dd, for example: 2009-11-12. If specified,
                search builds generated before this date.

            version (Optional[str]):
                Specify the build version to match. The character * can be used in
                the version string to do wildcard match. If not specified, all
                versions will be matched.

            status (Optional[str]):
                Status of the build to match. Valid build statuses are:
                SUCCESSFUL, FAILED, RECOMMENDED, CANCELLED, RUNNING, TIMEOUT.
                If left empty, any build status will be matched.

            user_id (Optional[int]):
                Match builds which is triggered by specified user.
                If not specified, builds triggered by any user will be matched.

            promoted_from_id (Optional[int]):
                Match builds promoted from specified build id if specified.

            request_id (Optional[int]):
                If specified, match builds with specified build request id.

        Returns:
            int: builds count.
        """
        params = dict()  # type: Dict[str, Union[str, int, bool]]

        if configuration_id:
            params['configuration_id'] = configuration_id

        if recursive:
            params['recursive'] = recursive

        if from_date:
            params['from_date'] = from_date

        if to_date:
            params['to_date'] = to_date

        if version:
            params['version'] = version

        if status:
            params['status'] = status

        if user_id:
            params['user_id'] = user_id

        if promoted_from_id:
            params['promoted_from_id'] = promoted_from_id

        if request_id:
            params['request_id'] = request_id

        response = self.quickbuild._request(
            'GET',
            'builds/count',
            callback=response2py,
            params=params,
        )

        return response

    def update(self, configuration: str) -> int:
        """
        Update build using XML configuration.

        Please note that the configuration element denotes id of the belonging
        configuration. Normally you do not need to create the XML from scratch,
        you may retrieve XML representation of the build, modify certain parts
        of the XML and post back to above url.

        Args:
            configuration (str): XML document.

        Returns:
            int: build id being updated.
        """
        response = self.quickbuild._request(
            'POST',
            'builds',
            callback=response2py,
            data=configuration,
        )

        return response

    def create(self, configuration: str) -> int:
        """
        Create a build using XML/JSON configuration.

        The configuration element denotes id of the belonging configuration.
        Normally you do not need to create the XML from scratch: you may
        retrieve XML representation of a templating build or using `get_info()`
        with content_type=ContentType.XML, remove the id element, modify certain
        parts and use it as configuration for create method.

        Args:
            configuration (str): XML/JSON configuration.

        Returns:
            int: build id of the the newly created build.

        Raises:
            QBError: configuration validation error
        """
        self.quickbuild._validate_for_id(configuration)
        return self.update(configuration)

    def delete(self, build_id: int) -> None:
        """
        Delete build.

        Args:
            build_id (int): build id.

        Returns:
            None
        """
        return self.quickbuild._request(
            'DELETE',
            'builds/{}'.format(build_id),
            callback=response2py,
        )
