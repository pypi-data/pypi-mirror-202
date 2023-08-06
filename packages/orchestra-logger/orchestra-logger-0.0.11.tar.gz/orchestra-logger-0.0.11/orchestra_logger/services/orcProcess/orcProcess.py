import inspect
from orchestra_logger.services.orchttp.orchttp import orcHTTP
from datetime import datetime

class orcProcess():
    def __init__(self, correlation_id:str, credentials:dict):
        self.correlation_id = correlation_id
        self.creds = credentials
        if 'apikey' not in self.creds:
            raise ValueError('The credentials object must be a dict that contains an apikey')
        self.client = orcHTTP(self.creds)
        self.kickoff()

    def kickoff(self):
        message = f'Orc process with correlation id {self.correlation_id} started'
        status = 'Running'
        data = {}
        stage = inspect.stack()[2][3]
        return self.sendMessage(message=message, status=status, stage=stage, data=data)

    def sendMessage(self, message: str, status: str, stage: str, data: dict):

        data = {**data, **{'message':message, 'status':status, 'stage': stage, 'timeUTC':datetime.now()}}
        response = self.client.send_message(self.correlation_id, data)
        return response

    def sendFailure(self, message:str = '', stage:str = 'Process', data:dict ={}):
        """Use this function to send a failure event for an entire process or a given stage"""
        status = 'Failed'
        stage = stage
        function_name__ = inspect.stack()[1][3]
        data['function'] = function_name__
        return self.sendMessage(message=message, status=status, stage=stage, data=data)

    def sendCompletion(self, message:str = '', stage:str = 'Process', data:dict ={}):
        """Use this function to send a completion event for an entire process or a given stage"""
        status = 'Complete'
        stage = stage
        function_name__ = inspect.stack()[1][3]
        data['function'] = function_name__
        return self.sendMessage(message=message, status=status, stage=stage, data=data)

    def sendStageComplete(self, message, data):
        """Use this function to send a failure event for an entire process"""
        status = 'Stage passed'
        stage = 'Process'
        function_name__ = inspect.stack()[1][3]
        data['function'] = function_name__
        return self.sendMessage(message=message, status=status, stage=stage, data=data)
