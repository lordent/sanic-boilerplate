import inspect

from functools import wraps
from marshmallow import Schema
from oad import openapi

from errors.request import (
    BadRequestQueryData,
    BadRequestBodyData,
)


def query(schema: Schema):
    def inner(func):
        parameters = inspect.signature(func).parameters
        if 'request' in parameters:
            request_pos = list(parameters.keys()).index('request')
        else:
            raise Exception("Missing required argument: 'request'")

        @wraps(func)
        async def wrapper(*args, **kwargs):
            request = args[request_pos]
            request['query'], errors = schema.load(request.raw_args)
            if errors:
                return BadRequestQueryData(errors=errors)
            return await func(*args, **kwargs)
        return wrapper
    return inner


def body(schema: Schema):
    def inner(func):
        parameters = inspect.signature(func).parameters
        if 'request' in parameters:
            request_pos = list(parameters.keys()).index('request')
        else:
            raise Exception("Missing required argument: 'request'")

        @openapi.request(schema=schema)
        @openapi.response({
            'examples': {
                'Body': {
                    'summary': 'Bad body data',
                    'value': {
                        'type': BadRequestBodyData.type,
                        'message': '',
                        'errors': schema.load({}).errors,
                    }
                },
            }
        }, status=400, schema={'type': 'object'})
        @wraps(func)
        async def wrapper(*args, **kwargs):
            request = args[request_pos]
            request['data'], errors = schema.loads(request.body)
            if errors:
                return BadRequestBodyData(errors=errors)
            return await func(*args, **kwargs)
        return wrapper
    return inner
