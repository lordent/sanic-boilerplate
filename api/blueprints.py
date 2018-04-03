from sanic import Blueprint

from api.content.welcome import WelcomeView
from api.info import handler_openapi


content = Blueprint('v1', url_prefix='/api/v1',
                    strict_slashes=True)

content.add_route(handler_openapi, uri='/swagger.json')
content.add_route(WelcomeView.as_view(), uri='/welcome')
