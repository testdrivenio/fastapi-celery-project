from fastapi import APIRouter

tdd_router = APIRouter(
    prefix="/tdd",
)

from . import views, models # noqa
