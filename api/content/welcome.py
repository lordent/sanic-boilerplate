from sanic import response
from sanic.views import HTTPMethodView
from marshmallow import Schema, fields

from helpers.request import validate
from oad import openapi


@openapi.doc({
    'description': 'Welcome view methods set example',
})
class WelcomeView(HTTPMethodView):

    class WelcomePost(Schema):
        message = fields.String(required=True)

    @openapi.doc({
        'summary': 'Welcome get method example',
    })
    @openapi.response()
    async def get(self, request):
        return response.json('Welcome!')

    @openapi.doc({
        'summary': 'Welcome post method example',
        'responses': {
            '200': {
                'description': 'Welcome result response',
            },
        },
    })
    @openapi.response(schema=WelcomePost(many=True))
    @validate.body(WelcomePost())
    async def post(self, request):
        return response.json(
            ['Done! Your message is `%s`' % request['data']['message']])
