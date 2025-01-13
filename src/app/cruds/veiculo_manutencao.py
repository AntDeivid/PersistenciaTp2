from sqlalchemy.orm import Session
from typing import List, Optional
from src.app.models.veiculo_manutencao import VeiculoManutencao

def create_veiculo_manutencao(session: Session, veiculo_manutencao: VeiculoManutencao) -> VeiculoManutencao:
    session.add(veiculo_manutencao)
    session.commit()
    session.refresh(veiculo_manutencao)
    return veiculo_manutencao

def get_veiculo_manutencoes(session: Session) -> List[VeiculoManutencao]:
    return session.query(VeiculoManutencao).all()

def get_veiculo_manutencao_by_id(session: Session, id: int) -> Optional[VeiculoManutencao]:
    return session.query(VeiculoManutencao).filter(VeiculoManutencao.id == id).first()

def delete_veiculo_manutencao(session: Session, id: int) -> bool:
    veiculo_manutencao = session.query(VeiculoManutencao).filter(VeiculoManutencao.id == id).first()
    if not veiculo_manutencao:
        return False
    session.delete(veiculo_manutencao)
    session.commit()
    return True
