from sanic.response import HTTPResponse

from app import app
from api.blueprints import content


@app.route('/')
async def handler(request):
    return HTTPResponse(status=200, body='Welcome to Sanic!')


app.blueprint(content)
