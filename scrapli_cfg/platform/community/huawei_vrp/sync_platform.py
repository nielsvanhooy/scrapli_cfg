"""scrapli_cfg.platform.core.huawei_vrp.sync_platform"""
from typing import Any, Callable, List, Optional

from scrapli.driver import NetworkDriver
from scrapli.response import MultiResponse, Response
from scrapli_cfg.diff import ScrapliCfgDiffResponse
from scrapli_cfg.exceptions import DiffConfigError
from scrapli_cfg.platform.base.sync_platform import ScrapliCfgPlatform
from scrapli_cfg.platform.community.huawei_vrp.base_platform import ScrapliCfgHuaweiVrpBase, CONFIG_SOURCES

from scrapli_cfg.response import ScrapliCfgResponse


class ScrapliCfgHuaweiVrp(ScrapliCfgPlatform, ScrapliCfgHuaweiVrpBase):
    def __init__(
        self,
        conn: NetworkDriver,
        *,
        config_sources: Optional[List[str]] = None,
        on_prepare: Optional[Callable[..., Any]] = None,
        filesystem: str = "flash:",
        cleanup_post_commit: bool = True,
        dedicated_connection: bool = False,
        ignore_version: bool = False,
    ) -> None:
        if config_sources is None:
            config_sources = CONFIG_SOURCES

        super().__init__(
            conn=conn,
            config_sources=config_sources,
            on_prepare=on_prepare,
            dedicated_connection=dedicated_connection,
            ignore_version=ignore_version,
        )

        self.filesystem = filesystem

        self._replace = False
        self._set = False

        self.candidate_config_filename = ""
        self._in_configuration_session = False

        self.cleanup_post_commit = cleanup_post_commit

    def _delete_candidate_config(self) -> Response:
        """
        Delete candidate config from the filesystem

        Args:
            N/A

        Returns:
            Response: response from deleting the candidate config

        Raises:
            N/A

        """
        delete_result = self.conn.send_config(
            config=f"rm {self.filesystem}{self.candidate_config_filename}",
            privilege_level="configuration",
        )
        return delete_result

    def get_version(self) -> ScrapliCfgResponse:
        response = self._pre_get_version()

        version_result = self.conn.send_command(command="display version")

        return self._post_get_version(
            response=response,
            scrapli_responses=[version_result],
            result=self._parse_version(device_output=version_result.result),
        )

    def get_config(self, source: str = "running") -> ScrapliCfgResponse:
        response = self._pre_get_config(source=source)

        if self._in_configuration_session is True:
            config_result = self.conn.send_config(config="run show configuration")
        else:
            config_result = self.conn.send_command(command="display current-configuration")

        return self._post_get_config(
            response=response,
            source=source,
            scrapli_responses=[config_result],
            result=config_result.result,
        )

    def load_config(self, config: str, replace: bool = False, **kwargs: Any) -> ScrapliCfgResponse:
        pass

    def abort_config(self) -> ScrapliCfgResponse:
        pass

    def commit_config(self, source: str = "running") -> ScrapliCfgResponse:
        pass

    def diff_config(self, source: str = "running") -> ScrapliCfgDiffResponse:
        scrapli_responses = []
        device_diff = ""
        source_config = ""

        diff_response = self._pre_diff_config(
            source=source, session_or_config_file=bool(self.candidate_config_filename)
        )

        try:
            diff_result = self.conn.send_config(config="show | compare")
            scrapli_responses.append(diff_result)
            if diff_result.failed:
                msg = "failed generating diff for config session"
                self.logger.critical(msg)
                raise DiffConfigError(msg)

            device_diff = diff_result.result

            source_config_result = self.get_config(source=source)
            source_config = source_config_result.result

            if isinstance(source_config_result.scrapli_responses, MultiResponse):
                # in this case this will always be a multiresponse or nothing (failure) but mypy
                # doesnt know that, hence the isinstance check
                scrapli_responses.extend(source_config_result.scrapli_responses)

            if source_config_result.failed:
                msg = "failed fetching source config for diff comparison"
                self.logger.critical(msg)
                raise DiffConfigError(msg)

        except DiffConfigError:
            pass

        return self._post_diff_config(
            diff_response=diff_response,
            scrapli_responses=scrapli_responses,
            source_config=self.clean_config(source_config),
            candidate_config=self.clean_config(self.candidate_config),
            device_diff=device_diff,
        )
