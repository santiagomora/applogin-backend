from starlette.applications import\
    Starlette
from .routes.auth import\
    routes as auth_routes
from starlette.routing import\
    Mount
from contextlib import\
    asynccontextmanager
from sqlalchemy import\
    create_engine
import os
from .exception.handlers import\
    exception_handlers
from starlette.middleware import\
    Middleware
from starlette.middleware.cors import\
    CORSMiddleware


@asynccontextmanager
async def lifespan(app):
    uri = 'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'\
        .format(**({"DB_USER":     os.getenv("POSTGRES_USER", ""),
                    "DB_PASSWORD": os.getenv("POSTGRES_PASSWORD", ""),
                    "DB_HOST":     os.getenv("POSTGRES_HOST", ""),
                    "DB_PORT":     os.getenv("POSTGRES_PORT", ""),
                    "DB_NAME":     os.getenv("POSTGRES_DB", "")}))
    yield {"engine": create_engine(uri)}

routes = [Mount("/auth", name='auth', routes=auth_routes)]

middleware = [Middleware(CORSMiddleware,
                         allow_origins=['*'],
                         allow_headers=['*'],
                         allow_methods=['GET', 'POST', 'OPTIONS'])]

app = Starlette(debug=True, routes=routes, lifespan=lifespan,
                exception_handlers=exception_handlers, middleware=middleware)
