import os

from .app import app


if os.environ.get('DEBUG', '').lower() in ('true', '1', 'y', 'yes'):
    app.config.DEBUG = True
