from fastapi import APIRouter

from app.routes import videos

router = APIRouter()

router.include_router(videos.router, prefix="/videos")