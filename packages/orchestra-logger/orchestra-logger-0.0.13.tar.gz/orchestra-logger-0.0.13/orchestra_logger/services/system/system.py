import logging
import sys
class systemInfo():
    def __init__(self):
        self.logger = logging.getLogger("orchestra.system_errors")

    def _check_python_deprecations(self):
        # type: () -> None
        version = sys.version_info[:2]

        if version == (3, 4) or version == (3, 5):
            self.logger.warning(
                "orchestra-sdk 0.0.1 will drop support for Python %s.",
                "{}.{}\nPlease upgrade to the latest version to continue receiving upgrades and bugfixes".format(*version),
            )
