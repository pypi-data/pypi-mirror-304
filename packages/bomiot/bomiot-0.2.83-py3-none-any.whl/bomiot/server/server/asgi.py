import os

from django.core.asgi import get_asgi_application
from bomiot.server.core.websocket import websocket_application
from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parent.parent

if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bomiot.server.server.settings')

http_application = get_asgi_application()


async def application(scope, receive, send):
    if scope['type'] in ['http', 'https']:
        await http_application(scope, receive, send)
    elif scope['type'] in ['websocket']:
        await websocket_application(scope, receive, send)
    else:
        raise Exception('Unknown Type' + scope['type'])