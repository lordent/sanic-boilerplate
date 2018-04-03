from sanic import response
from sanic.views import HTTPMethodView
from marshmallow import Schema, fields

from helpers.request import validate


class WelcomeView(HTTPMethodView):

    class PostSchema(Schema):
        message = fields.String(required=True)

    @staticmethod
    async def get(request):
        return response.json('Welcome!')

    @validate.body(PostSchema())
    async def post(self, request):
        return response.json(
            'Done! With message %s' % request['data']['message'])
