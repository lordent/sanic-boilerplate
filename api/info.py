from sanic import response
from oad.api import OpenAPIDoc

from app import app


async def handler_openapi(request):
    return response.json(
        OpenAPIDoc()
        .add_parameter('parameter_id', {
            'description': 'Welcome parameter',
        })
        .to_dict(app=app)
    )
