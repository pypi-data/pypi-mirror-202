import requests

class simpleHTTP:
    def __init__(self, base_url):
        self.base_url = base_url
        self.headers = None
        self.parameters = None

    def add_default_headers(self, headers):
        self.headers = headers
        return self

    def add_headers(self, new_headers):
        if self.headers:
            self.headers = {
                **self.headers,
                **new_headers
            }
            return
        self.headers = new_headers

    def add_parameters(self, new_params):
        if self.parameters:
            self.parameters = {
                **self.parameters,
                **new_params
            }
            return
        self.parameters = new_params

    def base_request(self, endpoint, method="POST", params=None, headers=None, body=None, data=None):
        full_url = self.base_url
        if endpoint:
            full_url = f"{full_url}/{endpoint}"
        if headers:
            self.add_headers(headers)
        if params:
            self.add_parameters(params)
        try:
            response = requests.request(method, full_url, params=self.parameters, headers=self.headers, json=body,
                                        data=data)
            print(response.text)
            return {**response.json(), **{'status_code': response.status_code, 'reason': response.reason}}

        except Exception as error:
            return {
                'status_code': 400,
                'error': str(error)
            }

