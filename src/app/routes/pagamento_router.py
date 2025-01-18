from fastapi import APIRouter

from src.app.models.pagamento import Pagamento
from src.app.repositories.pagamento_repository import PagamentoRepository

pagamento_router = APIRouter()
pagamento_router.prefix = "/api/pagamentos"
pagamento_router.tags = ["Pagamentos"]

pagamento_repository = PagamentoRepository()

@pagamento_router.post("/")
def create_pagamento(pagamento: Pagamento):
    return pagamento_repository.create(pagamento)

@pagamento_router.get("/")
def get_pagamentos():
    return pagamento_repository.get_all()

@pagamento_router.get("/{pagamento_id}")
def get_pagamento_by_id(pagamento_id: int):
    return pagamento_repository.get_by_id(pagamento_id)

@pagamento_router.put("/{pagamento_id}")
def update_pagamento(pagamento_id: int, pagamento_data: dict):
    return pagamento_repository.update(pagamento_id, pagamento_data)

@pagamento_router.delete("/{pagamento_id}")
def delete_pagamento(pagamento_id: int):
    return pagamento_repository.delete(pagamento_id)
