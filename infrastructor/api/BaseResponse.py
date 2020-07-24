import jsonpickle
from flask import Response


class BaseResponse(Response):
    def __init__(self, response, *args, **kwargs):
        if 'mimetype' not in kwargs and 'contenttype' not in kwargs:
            if isinstance(response, str):
                kwargs['mimetype'] = 'application/json'
        response_json = response
        if isinstance(response, str):
            if kwargs.get('status') is None or kwargs.get('status') == 200:
                response_json = jsonpickle.encode({'result': jsonpickle.decode(response), 'isSuccess': 'true'})
        return super(BaseResponse, self).__init__(response_json, **kwargs)
