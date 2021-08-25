from broadcaster import Broadcast
from fastapi import FastAPI

from project.config import settings

broadcast = Broadcast(settings.WS_MESSAGE_QUEUE)


def create_app() -> FastAPI:
    app = FastAPI()

    from project.logging import configure_logging
    configure_logging()

    # do this before loading routes
    from project.celery_utils import create_celery
    app.celery_app = create_celery()

    from project.users import users_router
    app.include_router(users_router)

    from project.tdd import tdd_router
    app.include_router(tdd_router)

    from project.ws import ws_router
    app.include_router(ws_router)

    from project.ws.views import register_socketio_app
    register_socketio_app(app)

    @app.on_event("startup")
    async def startup_event():
        await broadcast.connect()

    @app.on_event("shutdown")
    async def shutdown_event():
        await broadcast.disconnect()

    @app.get("/")
    async def root():
        return {"message": "Hello World"}

    return app
