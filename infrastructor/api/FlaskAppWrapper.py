import logging
from datetime import datetime

from flask import Flask, request
from flask_cors import CORS

from infrastructor.api import ErrorHandler
from infrastructor.api.BaseResponse import BaseResponse
from werkzeug.exceptions import HTTPException

from infrastructor.api.ControllerBase import ControllerBase
from models.configs.ApiConfig import ApiConfig


class EndpointAction(object):
    def __init__(self, action):
        self.action = action

    def __call__(self, *args, **kwargs):
        response = self.action(**kwargs)
        return response


def replace_last(source_string, replace_what, replace_with):
    head, _sep, tail = source_string.rpartition(replace_what)
    return head + replace_with + tail


class FlaskAppWrapper(object):
    def __init__(self,
                 api_config: ApiConfig,
                 handlers: ErrorHandler,
                 controllers: [ControllerBase]):
        self.app = None
        self.api_config = api_config
        self.handlers = handlers
        self.controllers = controllers
        # Application create operations
        self.create_application()

    # Application flask configurations and api endpoint registration
    def create_application(self):
        self.app = Flask(self.api_config.name)
        CORS(self.app, resources={r"/api/*": {"origins": "*"}})
        self.app.response_class = BaseResponse
        # self.deploymentApp.after_request_funcs.setdefault(None, []).append(self.after_request)

        self.register_error_handlers()

        self.register_api_endpoints()

    # Api endpoints registered with controller base
    def register_api_endpoints(self):
        for controller in self.controllers:
            api_name = replace_last(controller().__class__.__name__, 'Controller', '').lower()
            controller().register_api_endpoints(f'/api/{api_name}/', self.add_endpoint)

    def register_error_handlers(self):
        self.app.register_error_handler(HTTPException, self.handlers.handle_http_exception)
        self.app.register_error_handler(Exception, self.handlers.handle_exception)

    def run(self):
        self.app.run(debug=self.api_config.is_debug, host='0.0.0.0', port=self.api_config.port)
        # serve(self.deploymentApp, host="0.0.0.0", port=self.apiConfig.port)
        # if self.apiConfig.isDebug:
        #     self.deploymentApp.run(debug=self.apiConfig.isDebug, port=self.apiConfig.port)
        # else:
        #     serve(self.deploymentApp, host="localhost", port=self.apiConfig.port)
        # http_server = WSGIServer((self.apiConfig.name, self.apiConfig.port), self.deploymentApp)
        # http_server.serve_forever()

    def add_endpoint(self, endpoint=None, endpoint_name=None, handler=None, methods=None):
        self.app.add_url_rule(endpoint, endpoint_name, EndpointAction(handler), methods=methods)

    def after_request(self, response):
        """ Logging after every request. """
        logger = logging.getLogger("app.access")
        logger.info(
            "%s [%s] %s %s %s %s %s %s %s",
            request.remote_addr,
            datetime.utcnow().strftime("%d/%b/%Y:%H:%M:%S.%f")[:-3],
            request.method,
            request.path,
            request.scheme,
            response.status,
            response.content_length,
            request.referrer,
            request.user_agent,
        )
        return response
