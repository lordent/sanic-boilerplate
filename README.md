# Sanic Boilerplate

This projet proposes a kickstarter python project based on the [Sanic](https://github.com/channelcat/sanic) framework
It embeds :
- a custom query validation
- the [marshmallow](https://marshmallow.readthedocs.io/en/3.0/) schema validation
- an auto API documentation through @decorators based on [OAD](https://github.com/lordent/oad)

## Getting Started

To use this Boilerplate just clone the repo as follows :

```
git clone https://github.com/lordent/sanic-boilerplate.git
```

Once fetched, copy/paste the files to your local project repository and add your code (routes, ...). See the section [How to add routes](#how-to-add-routes)
Before running your app, don't forget to install the dependencies, see [Installing the dependencies](#installing-the-dependencies)

### Prerequisites

This boilerplate uses [Sanic](https://github.com/channelcat/sanic), so you must have Python 3.5 or higher installed

### Installing the dependencies

The dependencies are listed in ```requirements.txt```, you can simply install them with ```pip install -r requirements.txt```

If you do not intend to use [Sentry](https://sentry.io/welcome/), just remove ```raven``` and ```raven_aiohttp``` from the ```requirements.txt``` file, and don't forget to remove or comment the code in ``settings/sentry.py```

## How to add routes

Let's say you want to create a **GET** route **/foo** which displays **"hello John Doe"**, and a **POST** route which must pass a parameter "bar" :

Edit the file ```api/blueprints.py```, import a new package at the head of the file like this:
```
from api.content.foo import FooView
```

Then add a new route at the bottom of the file like this:
```
content.add_route(FooView.as_view(), uri='/foo')
```

Edit the file ```api/content/foo.py```, copy/paste the structure of the file ```welcome.py``` and adapt like this:

```
from sanic import response
from sanic.views import HTTPMethodView
from marshmallow import Schema, fields

from helpers.request import validate
from oad import openapi


class FooPost(Schema):
    """In this example, the POST method requires a "bar" parameter of type string
    More examples and tutorials can be found here : https://marshmallow.readthedocs.io/en/3.0/
    """
    bar = fields.String(required=True)


@openapi.doc({
    'description': 'The new route displaying "hello John Doe"',
})
class FooView(HTTPMethodView):

    @openapi.doc({
        'summary': 'Foo get method example',
    })
    @openapi.response()
    async def get(self, request, parameter_id):
        return response.json('hello John Doe!')

    @openapi.doc({
        'summary': 'Foo post method example',
    })
    @openapi.response({
        'description': 'Foo result response',
    }, schema=FooPost(many=True))
    @validate.body(FooPost())
    async def post(self, request, parameter_id):
        return response.json(
          {'message': 'Your message to the user'}
        )
```

Add a file ```api/tests/test_foo.py```, and write the pytest functions that make sense for you !

## Running the tests

You can test the code by executing ```py.test``` at the root of the Boilerplate. This will run the tests located under ```tests```, ```api/tests``` and ```helpers/tests```. Thanks to pytest auto-discovery features, your new tests will be automatically run
