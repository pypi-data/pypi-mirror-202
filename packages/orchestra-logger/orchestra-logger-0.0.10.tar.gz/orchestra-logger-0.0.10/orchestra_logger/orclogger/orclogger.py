import sys
import logging
from orchestra_logger.services.orcProcess.orcProcess import orcProcess

class orcLogger():
    def __init__(self, name=""):
        self.name = name

class httpClient():
    def __init__(self, baseUrl):
        self.baseUrl = baseUrl

class orcHttpClient(httpClient):
    def __init__(self):
        baseUrl = 'Orchestra URL'
        super().__init__(baseUrl)

    def kickoff_process(self, correlation_id):
        pass
        # Need to make an API call to orchestra to kick off a process


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




def run_example_process(correlation_id):
    #Instantiating the orcProcess kicks off an individual process
    orcProcessInstance = orcProcess(correlation_id)

    print('Starting complicated process')

    try:
        print('Trying something complicated')
    except Exception as e:
        print('Failed to do something complicated')
        orcProcessInstance.sendFailure(message = str(e))
    finally:
        print('Completed')
        orcProcessInstance.sendCompletion(message = 'Completed')
