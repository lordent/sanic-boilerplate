from errors.base import BaseErrorResponse


class BadRequestQueryData(BaseErrorResponse):
    type = 'BAD_QUERY_DATA'


class BadRequestBodyData(BaseErrorResponse):
    type = 'BAD_BODY_DATA'
