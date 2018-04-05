import pytest
from openapi_spec_validator import validate_spec
from sanic import Sanic, response
from sanic.views import HTTPMethodView
from sanic.request import Request

from oad import openapi


@pytest.yield_fixture
def fix_app(fix_doc_settings):
    app = Sanic('test_sanic_app', strict_slashes=True)

    @openapi.doc({
        'summary': 'Test summary text',
        'description': 'Test description',
    })
    @openapi.request()
    @openapi.response()
    @app.route('/test-parameter-int/<parameter:int>')
    async def test_handler(request: Request, parameter: int):
        return response.json({
            'parameter': parameter,
        })

    class TestHTTPMethodView(HTTPMethodView):
        @openapi.request({
            'summary': 'Test summary text',
            'description': 'Test description',
        }, content_documentation={
            'example': {
                'id': '4',
            },
        }, schema={
            'type': 'object',
            'properties': {
                'id': {
                    'type': 'integer',
                    'format': 'int64',
                    'example': '4',
                },
            },
        })
        @openapi.response()
        async def post(self, request, parameter: str):
            return response.json({
                'parameter': parameter,
                'success': True
            })

    app.add_route(TestHTTPMethodView.as_view(), '/test-view-doc')

    yield app


@pytest.fixture
def fix_test_client(loop, fix_app, test_client):
    return loop.run_until_complete(test_client(fix_app))


@pytest.fixture
def fix_spec(fix_app):
    return OpenAPISanic(app=fix_app).to_dict()
