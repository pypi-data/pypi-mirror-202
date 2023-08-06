import asyncio

from typing import Dict

from hypercorn import Config
from hypercorn.asyncio import serve
from hypercorn.typing import WSGIFramework, ASGIFramework
from hypercorn.middleware import AsyncioWSGIMiddleware


def asgi_wrapper(wsgi_app: WSGIFramework) -> ASGIFramework:
    return AsyncioWSGIMiddleware(
        wsgi_app,
        max_body_size=2 ** 32
    )


def run(asgi_app: ASGIFramework, config: Dict = None):
    return asyncio.run(serve(
        asgi_app, Config.from_mapping(config or {})
    ))
