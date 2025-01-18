from fastapi import APIRouter

from src.app.models.veiculo import Veiculo
from src.app.repositories.veiculo_repository import VeiculoRepository

veiculo_router = APIRouter()
veiculo_router.prefix = "/api/veiculos"
veiculo_router.tags = ["Veículos"]

veiculo_repository = VeiculoRepository()

@veiculo_router.post("/")
def create_veiculo(veiculo: Veiculo):
    return veiculo_repository.create(veiculo)

@veiculo_router.get("/")
def get_veiculos():
    return veiculo_repository.get_all()

@veiculo_router.get("/{veiculo_id}")
def get_veiculo_by_id(veiculo_id: int):
    return veiculo_repository.get_by_id(veiculo_id)

@veiculo_router.put("/{veiculo_id}")
def update_veiculo(veiculo_id: int, veiculo_data: dict):
    return veiculo_repository.update(veiculo_id, veiculo_data)

@veiculo_router.delete("/{veiculo_id}")
def delete_veiculo(veiculo_id: int):
    return veiculo_repository.delete(veiculo_id)