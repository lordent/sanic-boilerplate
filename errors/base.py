from marshmallow import Schema, fields
from sanic.response import HTTPResponse, json_dumps


class BaseError(Schema):
    type = fields.String(required=True)
    message = fields.String()
    errors = fields.Dict(
        values=fields.String(),
        keys=fields.String()
    )


class BaseErrorResponse(HTTPResponse):

    schema = BaseError()

    type = 'UNKNOWN'

    def __init__(self, message='', errors=None, **kwargs):

        data = self.schema.load(dict(
            type=self.type,
            message=message,
            errors=errors,
        )).data

        kwargs.setdefault('content_type', 'application/json')
        kwargs.setdefault('status', 400)

        super().__init__(json_dumps(data), **kwargs)
