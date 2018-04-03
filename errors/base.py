from sanic.response import HTTPResponse, json_dumps


class BaseErrorResponse(HTTPResponse):

    type = 'UNKNOWN'

    def __init__(self, message='', errors=None,
                 dumps=json_dumps, **kwargs):

        data = dict(
            type=self.type,
            message=message,
            errors=errors,
        )

        kwargs.setdefault('content_type', 'application/json')
        kwargs.setdefault('status', 400)

        super().__init__(dumps(data), **kwargs)
