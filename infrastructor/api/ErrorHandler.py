import json
import traceback


class ErrorHandlers:
    def __init__(self):
        self.separator = '|'
        self.default_content_type = "application/json"
        self.mime_type_string = "mimetype"

    def handle_http_exception(self, exception):
        """Return JSON instead of HTML for HTTP errors."""
        # start with the correct headers and status code from the error
        response = exception.get_response()
        # replace the body with JSON
        response.data = json.dumps({
            "result": "",
            "isSuccess": "false",
            "code": exception.code,
            "name": exception.name,
            "message": exception.description,
        })
        response.content_type = self.default_content_type
        return response

    def handle_exception(self, exception):
        """Return JSON instead of HTML for HTTP errors."""
        # start with the correct headers and status code from the error
        exception_traceback = traceback.format_exc()
        output = self.separator.join(exception.args)
        # replace the body with JSON
        response = json.dumps({
            "result": "",
            "isSuccess": "false",
            "message": output,
            "traceback": exception_traceback
        })
        # response.content_type = "application/json"
        return response, 500, {self.mime_type_string: self.default_content_type}
