from sanic import response
from helpers.openapi import SanicOpenAPIDoc, openapi

from app import app


@openapi.doc({
    'summary': 'OpenAPI documentation',
})
@openapi.response({
    'description': 'OpenAPI v3 json schema response',
}, schema={'type': 'object'})
async def handler_openapi(request):
    url_prefix = '/api/v1'
    return response.json(
        SanicOpenAPIDoc()
        .add_server(
            '%s://%s%s' % (
                request.scheme,
                request.headers['host'],
                url_prefix
            ),
        )
        .add_parameter('parameter_id', {
            'description': 'Welcome parameter',
        })
        .to_dict(app=app, url_prefix=url_prefix)
    )
