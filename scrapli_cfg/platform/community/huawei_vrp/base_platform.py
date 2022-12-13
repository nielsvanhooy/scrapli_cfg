"""scrapli_cfg.platform.community.huawei_vrp.base_platform"""
import re
from datetime import datetime
from logging import Logger, LoggerAdapter
from typing import TYPE_CHECKING

from scrapli_cfg.helper import strip_blank_lines
from scrapli_cfg.platform.community.huawei_vrp.patterns import VERSION_PATTERN

if TYPE_CHECKING:
    LoggerAdapterT = LoggerAdapter[Logger]  # pylint:disable=E1136
else:
    LoggerAdapterT = LoggerAdapter


CONFIG_SOURCES = [
    "running",
    "startup",
]


class ScrapliCfgHuaweiVrpBase:
    logger: LoggerAdapterT
    candidate_config: str
    candidate_config_filename: str
    _in_configuration_session: bool
    _replace: bool
    _set: bool
    filesystem: str

    @staticmethod
    def _parse_version(device_output: str) -> str:
        """
        Parse version string out of device output

        Args:
            device_output: output from show version command

        Returns:
            str: device version string

        Raises:
            N/A

        """
        version_string_search = re.search(pattern=VERSION_PATTERN, string=device_output)

        if not version_string_search:
            return ""

        version_string = version_string_search.groupdict()['version'] or ""
        return version_string

