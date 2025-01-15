import logging
from datetime import datetime
from sqlite3 import IntegrityError
from typing import Optional

from src.app.core.db.database import get_db
from src.app.models.pagamento import Pagamento


class PagamentoRepository:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def create(self, pagamento: Pagamento) -> Pagamento:
        try:
            with next(get_db()) as db:
                db.add(pagamento)
                db.commit()
                db.refresh(pagamento)
                return pagamento
        except IntegrityError:
            self.logger.error("Erro ao criar pagamento!")
            raise ValueError("Erro ao criar pagamento!")

    def get_all_no_pagination(self) -> list[Pagamento]:
        with next(get_db()) as db:
            self.logger.info("Buscando todos os pagamentos, sem paginação")
            return db.query(Pagamento).all()

    def get_all(
            self,
            data_inicial: Optional[datetime] = None,
            data_final: Optional[datetime] = None,
            pago: Optional[bool] = None,
            page: Optional[int] = 1,
            limit: Optional[int] = 10
    ):
        with next(get_db()) as db:
            query = db.query(Pagamento)
            if data_inicial and data_final:
                query = query.filter(Pagamento.vencimento >= data_inicial, Pagamento.vencimento <= data_final)
            if data_inicial:
                query = query.filter(Pagamento.vencimento == data_inicial)
            if pago is not None:
                query = query.filter(Pagamento.pago == pago)

            self.logger.info(f"Buscando pagamentos com filtros: data_inicial={data_inicial}, data_final={data_final}, pago={pago}")
            return query.offset((page - 1) * limit).limit(limit).all()

    def get_by_id(self, pagamento_id: int) -> Pagamento:
        with next(get_db()) as db:
            self.logger.info(f"Buscando pagamento de id {pagamento_id}")
            return db.query(Pagamento).filter(Pagamento.id == pagamento_id).first()

    def update(self, pagamento_id: int, pagamento_data: dict) -> Pagamento:
        with next(get_db()) as db:
            pagamento = db.query(Pagamento).filter(Pagamento.id == pagamento_id).first()
            if not pagamento:
                return None
            for key, value in pagamento_data.items():
                if hasattr(pagamento, key):
                    setattr(pagamento, key, value)
            db.commit()
            db.refresh(pagamento)
            self.logger.info(f"Pagamento de id {pagamento_id} atualizado")
            return pagamento

    def delete(self, pagamento_id: int) -> bool:
        with next(get_db()) as db:
            pagamento = db.query(Pagamento).filter(Pagamento.id == pagamento_id).first()
            if not pagamento:
                return False
            db.delete(pagamento)
            db.commit()
            self.logger.info(f"Pagamento de id {pagamento_id} deletado")
            return True