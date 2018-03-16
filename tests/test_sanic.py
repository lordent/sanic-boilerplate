import pytest

from app import app
import routes  # noqa
import middlewares  # noqa


@pytest.yield_fixture
def fix_app():
    yield app


@pytest.fixture
def fix_test_client(loop, fix_app, test_client):
    return loop.run_until_complete(test_client(fix_app))


async def test_index_returns_200(fix_test_client):
    response = await fix_test_client.get('/')
    assert response.status == 200
    assert await response.text() == 'Welcome to Sanic!'
