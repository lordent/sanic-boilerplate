import json
from tests.test_sanic import fix_app, fix_test_client


async def test_welcome(fix_test_client):
    parameter_id = 'test-parameter-value'
    response = await fix_test_client.get('/api/v1/welcome/%s' % parameter_id)
    assert response.status == 200
    assert await response.json() == 'Welcome!'

    response = await fix_test_client.post(
        '/api/v1/welcome/%s' % parameter_id,
        data=json.dumps({'message': 'Test message'})
    )
    assert response.status == 200
    assert await response.json() == [
        'Done! Your message is `%s`, parameter: `%s`' % (
            'Test message',
            parameter_id
        )
    ]
