from openapi_spec_validator import validate_spec

from oad import openapi
from oad.api.base import OpenAPIDoc


async def test_doc():

    info = {
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

    error_schema = {
        'type': 'object',
        'properties': {
            'type': {'type': 'string'},
            'message': {'type': 'string'},
            'errors': {'type': 'object'}
        },
    }

    error_response = {
        'description': 'Error response',
        'content': {
            'application/json': {
                'schema': {
                    '$ref': '#/components/schemas/Error'
                }
            }
        }
    }

    @openapi.doc({
        'summary': 'Test summary text',
        'description': 'Test description',
        'tags': ['test'],
        'parameters': [{
            '$ref': '#/components/parameters/TestParameter'
        }],
    })
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
    @openapi.response(
        status=400, schema={'$ref': '#/components/schemas/Error'})
    async def test_handler():
        return 'Ok!'

    assert await test_handler() == 'Ok!'

    doc = (
        OpenAPIDoc({
            'info': info,
        })
        .add_parameter('TestParameter')
        .add_tag('test', {'description': 'Test tag description'})
        .add_path(
            '/test/{TestParameter}', 'post',
            test_handler.__openapi__.documentation)
        .add_schema('Error', error_schema)
        .add_response('Error', error_response)
        .to_dict()
    )

    assert doc == {
        'openapi': '3.0.0',
        'info': info,
        'tags': [{
            'name': 'test',
            'description': 'Test tag description'
        }],
        'paths': {
            '/test/{TestParameter}': {
                'post': {
                    'tags': ['test'],
                    'parameters': [{
                        '$ref': '#/components/parameters/TestParameter'
                    }],
                    'responses': {
                        '400': {
                            'description': '',
                            'content': {
                                'application/json': {
                                    'schema': {
                                        '$ref': '#/components/schemas/Error'
                                    }
                                }
                            }
                        },
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
                    'summary': 'Test summary text',
                    'description': 'Test description'
                }
            }
        },
        'components': {
            'schemas': {
                'Error': {
                    'type': 'object',
                    'properties': {
                        'type': {
                            'type': 'string'
                        },
                        'message': {
                            'type': 'string'
                        },
                        'errors': {
                            'type': 'object'
                        }
                    }
                }
            },
            'parameters': {
                'TestParameter': {
                    'name': 'TestParameter',
                    'in': 'path',
                    'required': True,
                    'schema': {'type': 'string'},
                },
            },
            'responses': {
                'Error': error_response
            },
            'securitySchemes': {}
        }
    }

    validate_spec(doc)
