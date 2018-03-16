import os
import logging
from raven import Client
import raven_aiohttp
from raven.handlers.logging import SentryHandler
from raven.conf import setup_logging


if 'CENTRY_URL' in os.environ:
    client = Client(
        dsn=os.environ['CENTRY_URL'],
        transport=raven_aiohttp.AioHttpTransport,
    )
    handler = SentryHandler(client)
    handler.setLevel(logging.ERROR)
    setup_logging(handler)
