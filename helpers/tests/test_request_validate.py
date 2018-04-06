import datetime
import json

import pytest
from marshmallow import Schema, fields
from sanic import Sanic, response, views

from errors.request import (
    BadRequestQueryData,
    BadRequestBodyData,
)
from helpers.request import validate


@pytest.yield_fixture
def fix_app():
    app = Sanic(__name__, strict_slashes=True)

    class DataSchema(Schema):
        email = fields.Email(required=True)
        datetime = fields.DateTime(format='iso')

    @app.route('/test-query-body-validate')
    @validate.query(DataSchema())
    @validate.body(DataSchema())
    async def handler(request):
        return response.json(
            status=200,
            body={
                'query': DataSchema().dump(request['query']).data,
                'data': DataSchema().dump(request['data']).data,
            }
        )

    class View(views.HTTPMethodView):
        @validate.query(DataSchema())
        @validate.body(DataSchema())
        async def get(self, request, parameter):
            return response.json(
                status=200,
                body={
                    'parameter': parameter,
                    'query': DataSchema().dump(request['query']).data,
                    'data': DataSchema().dump(request['data']).data,
                }
            )

    app.add_route(View.as_view(), '/test-view-query-body-validate/<parameter>')

    yield app


@pytest.fixture
def fix_test_client(loop, fix_app, test_client):
    return loop.run_until_complete(test_client(fix_app))


async def fix_assets(fix_test_client, url, parameter=None):
    dt = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc,
        microsecond=0
    )

    response = await fix_test_client.get(url)
    assert response.status == 400
    assert await response.json() == {
        'type': BadRequestQueryData.type,
        'message': '',
        'errors': {
            'email': ['Missing data for required field.'],
        },
    }

    data = {
        'email': 'test@test.com',
        'datetime': 'bad string',
    }
    response = await fix_test_client.get(url, params=data)
    assert response.status == 400
    assert await response.json() == {
        'type': BadRequestQueryData.type,
        'message': '',
        'errors': {
            'datetime': ['Not a valid datetime.']
        },
    }

    data = {
        'email': 'test@test.com',
        'datetime': dt.isoformat(),
    }
    response = await fix_test_client.get(
        url,
        params=data, data=json.dumps({'datetime': 'bad string'}))
    assert response.status == 400
    assert await response.json() == {
        'type': BadRequestBodyData.type,
        'message': '',
        'errors': {
            'email': ['Missing data for required field.'],
            'datetime': ['Not a valid datetime.'],
        },
    }

    data = {
        'email': 'test@test.com',
        'datetime': dt.isoformat(),
    }
    response = await fix_test_client.get(
        url, params=data, data=json.dumps(data))
    assert response.status == 200
    assert await response.json() == {
        'query': data,
        'data': data,
        **({'parameter': parameter} if parameter else {})
    }


async def test_handler_validate(fix_test_client):
    await fix_assets(fix_test_client, '/test-query-body-validate')


async def test_view_handler_validate(fix_test_client):
    parameter = 'test parameter value'
    await fix_assets(
        fix_test_client,
        '/test-view-query-body-validate/%s' % parameter,
        parameter,
    )
