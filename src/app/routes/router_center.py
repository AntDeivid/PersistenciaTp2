from fastapi.routing import APIRouter

from src.app.routes.usuario_router import usuario_router

router = APIRouter()

router.include_router(usuario_router)