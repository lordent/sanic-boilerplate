import pytest
from openapi_spec_validator import validate_spec
from sanic import Sanic, response
from sanic.views import HTTPMethodView
from sanic.request import Request

from helpers.openapi import openapi, SanicOpenAPIDoc


@pytest.fixture
def fix_info():
    return {
        'title': 'Test',
        'description': 'Test api description',
        'termsOfService': 'Test terms',
        'contact': {
            'name': 'Tester',
            'url': 'http://example.com',
            'email': 'test@example.com'
        },
        'license': {
            'name': 'Apache 2.0',
            'url': 'http://www.apache.org/licenses/LICENSE-2.0.html'
        },
        'version': '1.0'
    }


@pytest.yield_fixture
def fix_app():
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
        async def post(self, request: Request, parameter: str):
            return response.json({
                'parameter': parameter,
                'success': True
            })

    app.add_route(TestHTTPMethodView.as_view(), '/test-view-doc/<parameter>')

    yield app


@pytest.fixture
def fix_test_client(loop, fix_app, test_client):
    return loop.run_until_complete(test_client(fix_app))


@pytest.fixture
def fix_spec(fix_app, fix_info):
    return SanicOpenAPIDoc({
        'info': fix_info,
    }).to_dict(app=fix_app)


async def test_sanic_openapi(fix_spec):
    assert fix_spec == {
        'openapi': '3.0.0',
        'info': {
            'title': 'Test',
            'description': 'Test api description',
            'termsOfService': 'Test terms',
            'contact': {
                'name': 'Tester',
                'url': 'http://example.com',
                'email': 'test@example.com'
            },
            'license': {
                'name': 'Apache 2.0',
                'url': 'http://www.apache.org/licenses/LICENSE-2.0.html'
            },
            'version': '1.0'
        },
        'tags': [],
        'paths': {
            '/test-parameter-int/{parameter}': {
                'get': {
                    'responses': {
                        '200': {
                            'description': '',
                            'content': {
                                'application/json': {
                                    'schema': {
                                        'type': 'string'
                                    }
                                }
                            }
                        }
                    },
                    'requestBody': {
                        'content': {
                            'application/json': {
                                'schema': {
                                    'type': 'string'
                                }
                            }
                        }
                    },
                    'summary': 'Test summary text',
                    'description': 'Test description',
                    'tags': [],
                    'parameters': [{
                        '$ref': '#/components/parameters/parameter'
                    }]
                }
            },
            '/test-view-doc/{parameter}': {
                'post': {
                    'responses': {
                        '200': {
                            'description': '',
                            'content': {
                                'application/json': {
                                    'schema': {
                                        'type': 'string'
                                    }
                                }
                            }
                        }
                    },
                    'requestBody': {
                        'content': {
                            'application/json': {
                                'schema': {
                                    'type': 'object',
                                    'properties': {
                                        'id': {
                                            'type': 'integer',
                                            'format': 'int64',
                                            'example': '4'
                                        }
                                    }
                                },
                                'example': {
                                    'id': '4'
                                }
                            }
                        },
                        'description': 'Test description'
                    },
                    'tags': []
                },
                'parameters': [{
                    '$ref': '#/components/parameters/parameter'
                }]
            }
        },
        'components': {
            'schemas': {},
            'parameters': {
                'parameter': {
                    'name': 'parameter',
                    'in': 'path',
                    'required': True,
                    'schema': {
                        'type': 'string'
                    }
                }
            },
            'responses': {},
            'securitySchemes': {}
        }
    }


async def test_sanic_openapi_validation(fix_spec):
    validate_spec(fix_spec)
