import asyncio

from typing import Dict, Union

from hypercorn import Config
from hypercorn.asyncio import serve
from hypercorn.typing import WSGIFramework, ASGIFramework
from hypercorn.middleware import AsyncioWSGIMiddleware


def asgi_wrapper(wsgi_app: WSGIFramework) -> ASGIFramework:
    return AsyncioWSGIMiddleware(
        wsgi_app,
        max_body_size=2 ** 32
    )


def run(app: Union[ASGIFramework | WSGIFramework], config: Dict = None):
    from graphql_service_framework.middleware import ServiceMeshMiddleware

    if isinstance(app, ServiceMeshMiddleware):
        asgi_app = asgi_wrapper(app)
    else:
        asgi_app = app

    return asyncio.run(serve(
        asgi_app, Config.from_mapping(config or {})
    ))
