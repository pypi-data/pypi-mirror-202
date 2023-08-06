from orchestra_logger.services.http.http import HTTP

class orcHTTP(HTTP):
    def __init__(self, creds):
        baseUrl = 'https://public-api-orchestra.azurewebsites.net'
        super().__init__(baseUrl)
        self.add_default_headers({"Authorization": f"Bearer {creds['apikey']}"})

    def kickoff_process(self, correlation_id):
        """TODO: do we add a client ID here?"""
        response = self.base_request(method='POST', endpoint='integrations/selfhosted/kickoff_process', data = {'correlation_id':correlation_id})
        return response

    def send_message(self, correlation_id, data):
        data['correlation_id'] = correlation_id
        print(data)
        response = self.base_request(method='POST', endpoint='integrations/selfhosted/log_event', data = data)
        return response


