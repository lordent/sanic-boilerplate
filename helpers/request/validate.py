from sanic.request import Request
from functools import wraps
from marshmallow import Schema

from errors.request import (
    BadRequestQueryData,
    BadRequestBodyData,
)


def query(schema: Schema):
    def inner(func):
        @wraps(func)
        def wrapper(request: Request, *args, **kwargs):
            request['query'], errors = schema.load(request.raw_args)
            if errors:
                return BadRequestQueryData(errors=errors)
            return func(request, *args, **kwargs)
        return wrapper
    return inner


def body(schema: Schema):
    def inner(func):
        @wraps(func)
        def wrapper(request: Request, *args, **kwargs):
            request['data'], errors = schema.loads(request.body)
            if errors:
                return BadRequestBodyData(errors=errors)
            return func(request, *args, **kwargs)
        return wrapper
    return inner
