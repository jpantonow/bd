from fastapi import APIRouter

from app.api.routes import items, login, users, utils,refeicao, dieta

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(utils.router, prefix="/utils", tags=["utils"])
# api_router.include_router(items.router, prefix="/items", tags=["items"])
api_router.include_router(refeicao.router, prefix="/refeicoes", tags=["refeicoes"])
api_router.include_router(dieta.router, prefix="/dietas", tags=["dietas"])
