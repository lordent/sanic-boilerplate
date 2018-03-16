from app import app
import routes  # noqa
import middlewares  # noqa


def test_cors_headers():
    request, response = app.test_client.get('/')
    assert 'Access-Control-Allow-Origin' in response.headers
    assert 'Access-Control-Allow-Headers' in response.headers
    assert 'Access-Control-Allow-Methods' in response.headers
