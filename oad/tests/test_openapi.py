import pytest
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

    """
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
    """

    @openapi.doc({
        'summary': 'Test summary text',
        'description': 'Test description',
    })
    @openapi.response()
    async def test_handler():
        return 'Ok!'

    assert hasattr(test_handler, '__openapi__')
    assert await test_handler() == 'Ok!'

    doc = (
        OpenAPIDoc({
            'info': info,
        })
        .add_path('/test', 'get', test_handler.__openapi__.documentation)
        .to_dict()
    )

    """
    assert doc == {
        'openapi': '3.0.0',
        'info': info,
        'tags': [],
        'paths': {
            '/test/': {
                'get': {
                    'responses': {
                        '200': {
                            'content': {
                                'application/json': {
                                    'schema': {'type': 'string'}
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
                                'example': {'id': '4'}
                            }
                        },
                        'summary': 'Test summary text',
                        'description': 'Test description'
                    },
                    'summary': 'Test summary text',
                    'description': 'Test description'
                }
            }
        },
        'components': {
            'schemas': {},
            'parameters': {},
            'responses': {},
            'securitySchemes': {}
        }
    }
    """

    validate_spec(doc)
