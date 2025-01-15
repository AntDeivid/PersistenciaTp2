import logging
from sqlite3 import IntegrityError
from typing import Optional

from sqlalchemy.orm import joinedload

from src.app.core.db.database import get_db
from src.app.models.contrato import Contrato


class ContratoRepository:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def create(self, contrato: Contrato) -> Contrato:
        try:
            with next(get_db()) as db:
                db.add(contrato)
                db.commit()
                db.refresh(contrato)
                return contrato
        except IntegrityError:
            self.logger.error("Erro ao criar contrato!")
            raise ValueError("Erro ao criar contrato!")

    def get_all_no_pagination(self) -> list[Contrato]:
        with next(get_db()) as db:
            self.logger.info("Buscando todos os contratos, sem paginação")
            return db.query(Contrato).all()

    def get_all(self, page: Optional[int] = 1, limit: Optional[int] = 10) -> list[Contrato]:
        with next(get_db()) as db:
            self.logger.info("Buscando todos os contratos")
            return db.query(Contrato).offset((page - 1) * limit).limit(limit).all()

    def get_by_id(self, contrato_id: int) -> Contrato:
        with next(get_db()) as db:
            self.logger.info(f"Buscando contrato de id {contrato_id}")
            return db.query(Contrato).filter(Contrato.id == contrato_id).first()

    def get_contratos_by_usuario_veiculo(self) -> list[Contrato]:
        with next(get_db()) as db:
            self.logger.info("Buscando todos os contratos com usuario e veiculo")
            return db.query(Contrato).options(joinedload(Contrato.usuario), joinedload(Contrato.veiculo)).all()

    def get_contratos_by_usuario_id(self, usuario_id: int) -> list[Contrato]:
        with next(get_db()) as db:
            self.logger.info(f"Buscando todos os contratos com usuario de id {usuario_id}")
            return db.query(Contrato).filter(Contrato.usuario_id == usuario_id).options(joinedload(Contrato.usuario), joinedload(Contrato.veiculo)).all()


    def get_quantidade_contratos(self) -> int:
        with next(get_db()) as db:
            self.logger.info("Buscando quantidade de contratos")
            return db.query(Contrato).count()

    def update(self, contrato_id: int, contrato_data: dict) -> Contrato:
        with next(get_db()) as db:
            contrato = db.query(Contrato).filter(Contrato.id == contrato_id).first()
            if not contrato:
                return None
            for key, value in contrato_data.items():
                if hasattr(contrato, key):
                    setattr(contrato, key, value)
            db.commit()
            db.refresh(contrato)
            self.logger.info(f"Contrato de id {contrato_id} atualizado")
            return contrato

    def delete(self, contrato_id: int) -> bool:
        with next(get_db()) as db:
            contrato = db.query(Contrato).filter(Contrato.id == contrato_id).first()
            if not contrato:
                return False
            db.delete(contrato)
            db.commit()
            self.logger.info(f"Contrato de id {contrato_id} deletado")
            return True