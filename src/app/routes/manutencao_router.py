from fastapi import APIRouter

from src.app.models.manutencao import Manutencao
from src.app.repositories.manutencao_repository import ManutencaoRepository

manutencao_router = APIRouter()
manutencao_router.prefix = "/api/manutencoes"
manutencao_router.tags = ["Manutenções"]

manutencao_repository = ManutencaoRepository()

@manutencao_router.post("/")
def create_manutencao(manutencao: Manutencao):
    return manutencao_repository.create(manutencao)

@manutencao_router.get("/")
def get_manutencoes():
    return manutencao_repository.get_all()

@manutencao_router.get("/{manutencao_id}")
def get_manutencao_by_id(manutencao_id: int):
    return manutencao_repository.get_by_id(manutencao_id)

@manutencao_router.put("/{manutencao_id}")
def update_manutencao(manutencao_id: int, manutencao_data: dict):
    return manutencao_repository.update(manutencao_id, manutencao_data) 

@manutencao_router.delete("/{manutencao_id}")
def delete_manutencao(manutencao_id: int):
    return manutencao_repository.delete(manutencao_id)