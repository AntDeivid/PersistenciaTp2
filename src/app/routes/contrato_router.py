from fastapi import APIRouter

from src.app.models.contrato import Contrato 
from src.app.repositories.contrato_repository import ContratoRepository

contrato_router = APIRouter()
contrato_router.prefix = "/api/contratos"
contrato_router.tags = ["Contratos"]

contrato_repository = ContratoRepository()

@contrato_router.post("/")
def create_contrato(contrato: Contrato):
    return contrato_repository.create(contrato)

@contrato_router.get("/")
def get_contratos():
    return contrato_repository.get_all()

@contrato_router.get("/{contrato_id}")
def get_contrato_by_id(contrato_id: int):
    return contrato_repository.get_by_id(contrato_id)

@contrato_router.put("/{contrato_id}")
def update_contrato(contrato_id: int, contrato_data: dict):
    return contrato_repository.update(contrato_id, contrato_data)

@contrato_router.delete("/{contrato_id}")
def delete_contrato(contrato_id: int):
    return contrato_repository.delete(contrato_id)
