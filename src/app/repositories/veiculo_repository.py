import logging
from sqlite3 import IntegrityError
from typing import Optional

from sqlalchemy.orm import joinedload

from src.app.core.db.database import get_db
from src.app.models.manutencao import Manutencao
from src.app.models.veiculo import Veiculo
from src.app.models.veiculo_manutencao import VeiculoManutencao


class VeiculoRepository:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def create(self, veiculo: Veiculo) -> Veiculo:
        try:
            with next(get_db()) as db:
                db.add(veiculo)
                db.commit()
                db.refresh(veiculo)
                return veiculo
        except IntegrityError:
            self.logger.error("Erro ao criar veículo!")
            raise ValueError("Erro ao criar veículo!")

    def get_all_no_pagination(self) -> list[Veiculo]:
        with next(get_db()) as db:
            self.logger.info("Buscando todos os veículos")
            return db.query(Veiculo).all()

    def get_by_id(self, veiculo_id: int) -> Veiculo:
        with next(get_db()) as db:
            self.logger.info(f"Buscando veículo de id {veiculo_id}")
            return db.query(Veiculo).filter(Veiculo.id == veiculo_id).first()

    def get_veiculos_com_manutencoes(self) -> list[Veiculo]:
        with next(get_db()) as db:
            return db.query(Veiculo).options(joinedload(Veiculo.manutencoes)).all()

    def get_veiculos_by_tipo_manutencao(self, tipo_manutencao: str) -> list[Veiculo]:
        with next(get_db()) as db:
            return db.query(Veiculo).join(VeiculoManutencao).join(Manutencao).filter(
                Manutencao.tipo_manutencao == tipo_manutencao).options(joinedload(Veiculo.manutencoes)).all()

    def get_quantidade_veiculos(self) -> int:
        with next(get_db()) as db:
            self.logger.info("Buscando quantidade de veículos")
            return db.query(Veiculo).count()

    def get_all(self,
        tipo: Optional[str] = None,
        marca: Optional[str] = None,
        modelo: Optional[str] = None,
        ano: Optional[int] = None,
        page: Optional[int] = 1,
        limit: Optional[int] = 10
    ) -> list[Veiculo]:
        with next(get_db()) as db:
            query = db.query(Veiculo)
            if tipo:
                query = query.filter(Veiculo.tipo == tipo)
            if marca:
                query = query.filter(Veiculo.marca == marca)
            if modelo:
                query = query.filter(Veiculo.modelo == modelo)
            if ano:
                query = query.filter(Veiculo.ano == ano)
            self.logger.info(f"Buscando veículos com filtro tipo={tipo}, marca={marca}, modelo={modelo}, ano={ano}")
            return query.offset((page - 1) * limit).limit(limit).all()

    def update(self, veiculo_id: int, veiculo_data: dict) -> Veiculo:
        with next(get_db()) as db:
            veiculo = db.query(Veiculo).filter(Veiculo.id == veiculo_id).first()
            if not veiculo:
                return None
            for key, value in veiculo_data.items():
                if hasattr(veiculo, key):
                    setattr(veiculo, key, value)
            db.commit()
            db.refresh(veiculo)
            self.logger.info(f"Veículo de id {veiculo_id} atualizado")
            return veiculo

    def delete(self, veiculo_id: int) -> bool:
        with next(get_db()) as db:
            veiculo = db.query(Veiculo).filter(Veiculo.id == veiculo_id).first()
            if not veiculo:
                return False
            db.delete(veiculo)
            db.commit()
            self.logger.info(f"Veículo de id {veiculo_id} deletado")
            return True