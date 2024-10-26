from fastapi import FastAPI
from app.routers import user
from app.middleware.correlation_id import CorrelationIdMiddleware
from app.core.config import settings
from app.core.security import add_cors
from app.utils.logger import logger

def create_app():
    app = FastAPI(title="User API")

    # Include routers
    app.include_router(user.router)

    # Add middleware
    app.add_middleware(CorrelationIdMiddleware)

    # Add CORS settings
    add_cors(app)

    # Health check endpoint
    @app.get("/healthcheck")
    async def healthcheck():
        return {"status": "ok"}

    return app

app = create_app()
