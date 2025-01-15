import logging
from sqlite3 import IntegrityError

from src.app.core.db.database import get_db
from src.app.models.manutencao import Manutencao


class ManutencaoRepository:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def create(self, manutencao: Manutencao) -> Manutencao:
        try:
            with next(get_db()) as db:
                db.add(manutencao)
                db.commit()
                db.refresh(manutencao)
                return manutencao
        except IntegrityError:
            self.logger.error("Erro ao criar manutenção!")
            raise ValueError("Erro ao criar manutenção!")

    def get_all(self) -> list[Manutencao]:
        with next(get_db()) as db:
            self.logger.info("Buscando todas as manutenções")
            return db.query(Manutencao).all()

    def get_by_id(self, manutencao_id: int) -> Manutencao:
        with next(get_db()) as db:
            self.logger.info(f"Buscando manutenção de id {manutencao_id}")
            return db.query(Manutencao).filter(Manutencao.id == manutencao_id).first()

    def get_quantidade_manutencoes(self) -> int:
        with next(get_db()) as db:
            self.logger.info("Buscando quantidade de manutenções")
            return db.query(Manutencao).count()

    def update(self, manutencao_id: int, manutencao_data: dict) -> Manutencao:
        with next(get_db()) as db:
            manutencao = db.query(Manutencao).filter(Manutencao.id == manutencao_id).first()
            if not manutencao:
                return None
            for key, value in manutencao_data.items():
                if hasattr(manutencao, key):
                    setattr(manutencao, key, value)
            db.commit()
            db.refresh(manutencao)
            self.logger.info(f"Manutenção de id {manutencao_id} atualizada")
            return manutencao

    def delete(self, manutencao_id: int) -> bool:
        with next(get_db()) as db:
            manutencao = db.query(Manutencao).filter(Manutencao.id == manutencao_id).first()
            if not manutencao:
                return False
            db.delete(manutencao)
            db.commit()
            self.logger.info(f"Manutenção de id {manutencao_id} deletada")
            return True