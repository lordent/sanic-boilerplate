from sanic import response
from oad import api, openapi

from app import app


@openapi.doc({
    'summary': 'OpenAPI documentation',
})
@openapi.response({
    'description': 'OpenAPI v3 json schema response',
}, schema={'type': 'object'})
async def handler_openapi(request):
    return response.json(
        api.OpenAPIDoc()
        .add_parameter('parameter_id', {
            'description': 'Welcome parameter',
        })
        .to_dict(app=app)
    )
