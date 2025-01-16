from fastapi import APIRouter

from src.app.models.veiculo_manutencao import VeiculoManutencao
from src.app.repositories.veiculo_manutencao_repository import VeiculoManutencaoRepository

veiculo_manutencao_router = APIRouter()
veiculo_manutencao_router.prefix = "/api/veiculos_manutencoes"
veiculo_manutencao_router.tags = ["Veículos Manutenções"]

veiculo_manutencao_repository = VeiculoManutencaoRepository()

@veiculo_manutencao_router.post("/")
def create_veiculo_manutencao(veiculo_manutencao: VeiculoManutencao):
    return veiculo_manutencao_repository.create(veiculo_manutencao)

@veiculo_manutencao_router.get("/")
def get_veiculos_manutencoes():
    return veiculo_manutencao_repository.get_all()

@veiculo_manutencao_router.get("/{veiculo_manutencao_id}")
def get_veiculo_manutencao_by_id(veiculo_manutencao_id: int):
    return veiculo_manutencao_repository

@veiculo_manutencao_router.put("/{veiculo_manutencao_id}")
def update_veiculo_manutencao(veiculo_manutencao_id: int, veiculo_manutencao_data: dict):
    return veiculo_manutencao_repository.update(veiculo_manutencao_id, veiculo_manutencao_data)

@veiculo_manutencao_router.delete("/{veiculo_manutencao_id}")
def delete_veiculo_manutencao(veiculo_manutencao_id: int):
    return veiculo_manutencao_repository.delete(veiculo_manutencao_id)