from sanic import response
from oad.api import OpenAPIDoc

from app import app


async def handler_openapi(request):
    return response.json(
        OpenAPIDoc()
        .to_dict(app=app)
    )
