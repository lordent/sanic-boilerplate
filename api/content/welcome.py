from sanic import response
from sanic.views import HTTPMethodView
from marshmallow import Schema, fields

from helpers.request import validate
from oad import openapi


class WelcomePost(Schema):
    message = fields.String(required=True)


@openapi.doc({
    'description': 'Welcome view methods set example',
})
class WelcomeView(HTTPMethodView):

    @openapi.doc({
        'summary': 'Welcome get method example',
    })
    @openapi.response()
    async def get(self, request, parameter_id):
        return response.json('Welcome!')

    @openapi.doc({
        'summary': 'Welcome post method example',
    })
    @openapi.response({
        'description': 'Welcome result response',
    }, schema=WelcomePost(many=True))
    @validate.body(WelcomePost())
    async def post(self, request, parameter_id):
        return response.json(
            [
                'Done! Your message is `%s`, parameter: `%s`' % (
                    request['data']['message'], parameter_id
                )
            ]
        )
