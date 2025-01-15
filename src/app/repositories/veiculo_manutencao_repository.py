import logging
from sqlite3 import IntegrityError

from src.app.core.db.database import get_db
from src.app.models.veiculo_manutencao import VeiculoManutencao


class VeiculoManutencaoRepository:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def create(self, veiculo_manutencao: VeiculoManutencao) -> VeiculoManutencao:
        try:
            with next(get_db()) as db:
                db.add(veiculo_manutencao)
                db.commit()
                db.refresh(veiculo_manutencao)
                return veiculo_manutencao
        except IntegrityError:
            self.logger.error("Erro ao criar veículo_manutencao!")
            raise ValueError("Erro ao criar veículo_manutencao!")

    def get_all(self) -> list[VeiculoManutencao]:
        with next(get_db()) as db:
            self.logger.info("Buscando todos os veículos_manutencao")
            return db.query(VeiculoManutencao).all()

    def get_by_id(self, veiculo_manutencao_id: int) -> VeiculoManutencao:
        with next(get_db()) as db:
            self.logger.info(f"Bucando veículo_manutencao de id {veiculo_manutencao_id}")
            return db.query(VeiculoManutencao).filter(VeiculoManutencao.id == veiculo_manutencao_id).first()

    def get_quantidade_veiculos_manutencao(self) -> int:
        with next(get_db()) as db:
            self.logger.info("Buscando quantidade de veículos_manutencao")
            return db.query(VeiculoManutencao).count()

    def update(self, veiculo_manutencao_id: int, veiculo_manutencao_data: dict) -> VeiculoManutencao:
        with next(get_db()) as db:
            veiculo_manutencao = db.query(VeiculoManutencao).filter(VeiculoManutencao.id == veiculo_manutencao_id).first()
            if not veiculo_manutencao:
                return None
            for key, value in veiculo_manutencao_data.items():
                if hasattr(veiculo_manutencao, key):
                    setattr(veiculo_manutencao, key, value)
            db.commit()
            db.refresh(veiculo_manutencao)
            self.logger.info(f"Veículo_manutencao de id {veiculo_manutencao_id} atualizado")
            return veiculo_manutencao

    def delete(self, veiculo_manutencao_id: int) -> bool:
        with next(get_db()) as db:
            veiculo_manutencao = db.query(VeiculoManutencao).filter(VeiculoManutencao.id == veiculo_manutencao_id).first()
            if not veiculo_manutencao:
                return False
            db.delete(veiculo_manutencao)
            db.commit()
            self.logger.info(f"Veículo_manutencao de id {veiculo_manutencao_id} deletado")
            return True