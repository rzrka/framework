import quopri
from wsgiref.util import setup_testing_defaults

class Application:

    def decode_value(val):
        val_b = bytes(val.replace('%', '=').replace("+", " "), 'UTF-8')
        val_decode_str = quopri.decodestring(val_b)
        return val_decode_str.decode('UTF-8')

    def add_route(self, url):
        def inner(view):
            self.urlpatterns[url] = view

        return inner

    def parse_input_data(self, data: str):
        result = {}
        if data:
            params = data.split('&')

            for item in params:
                k, v = item.split('=')
                result[k] = v
        return result

    def parse_wsgi_input_data(self, data: bytes):
        result = {}
        if data:
            data_str = data.decode(encoding='utf-8')
            result = self.parse_input_data(data_str)
        return result

    def get_wsgi_input_data(self, env):
        content_length_data = env.get('CONTENT_LENGTH')
        content_length = int(content_length_data) if content_length_data else 0
        data = env['wsgi.input'].read(content_length) if content_length > 0 else b''
        return data

    def __init__(self, urlpatterns: dict ,front_controllers: list):
        '''
        :param urlpatterns: словарь связок url: view
        :param front_controllers: список front controllers
        '''
        self.urlpatterns = urlpatterns
        self.front_controllers = front_controllers

    def __call__(self, environ, start_response):
        setup_testing_defaults(environ)
        path = environ['PATH_INFO']
        if not path.endswith('/'):
            path += '/'

        method = environ['REQUEST_METHOD']
        data = self.get_wsgi_input_data(environ)
        data = self.parse_wsgi_input_data(data)

        query_string = environ['QUERY_STRING']
        request_params = self.parse_input_data(query_string)

        if path in self.urlpatterns:
            view = self.urlpatterns[path]
            request = {}
            request['method'] = method
            request['data'] = data
            request['request_params'] = request_params
            for front_controller in self.front_controllers:
                front_controller(request)
            code, body = view(request)
            start_response(code, [('Content-Type', 'text/html')])
            return [body.encode('utf-8')]
        else:
            start_response('404 NOT FOUND', [('Content-Type', 'text/html')])
            return [b'Not Found']


class DebugApplication(Application):

    def __init__(self, urlpatterns: dict, front_controllers: list):
        self.application = Application(urlpatterns, front_controllers)
        super().__init__(urlpatterns, front_controllers)

    def __call__(self, environ, start_response):
        print(environ)
        return self.application(environ, start_response)

class FakeApplication(Application):

    def __init__(self, urlpatterns, front_controllers):
        self.application = Application(urlpatterns, front_controllers)
        super().__init__(urlpatterns, front_controllers)

    def __call__(self, environ, start_response):
        start_response('200 OK', [('Content-Type', 'text/html')])
        return [b'Hello from Fake']