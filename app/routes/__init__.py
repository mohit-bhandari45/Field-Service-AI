from .api_routes import router as api_router
from .auth_routes.auth_routes import router as auth_router

all_routers = [(api_router, "/api"), (auth_router, "/auth")]