from oad import openapi
from oad.api.base import OpenAPIDoc


@openapi.doc({
    'summary': 'Test summary text',
    'description': 'Test description',
})
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
async def test_handler():
    return 'Ok!'

doc = (
    OpenAPIDoc()
    .add_path(
        '/test/',
        'get',
        test_handler.__openapi__.documentation
    )
    .to_dict()
)

print(doc)
