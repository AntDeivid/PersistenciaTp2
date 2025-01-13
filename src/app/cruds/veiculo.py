from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from src.app.models.veiculo import Veiculo
from typing import List, Optional

def create_veiculo(session: Session, veiculo: Veiculo) -> Veiculo:
    session.add(veiculo)
    try:
        session.commit()
        session.refresh(veiculo)
        return veiculo
    except IntegrityError:
        session.rollback()
        raise ValueError("Placa já cadastrada!")

def get_veiculos(session: Session) -> List[Veiculo]:
    return session.query(Veiculo).all()

def get_veiculo_by_id(session: Session, veiculo_id: int) -> Optional[Veiculo]:
    return session.query(Veiculo).filter(Veiculo.id == veiculo_id).first()

def update_veiculo(session: Session, veiculo_id: int, veiculo_data: dict) -> Optional[Veiculo]:
    veiculo = session.query(Veiculo).filter(Veiculo.id == veiculo_id).first()
    if not veiculo:
        return None
    for key, value in veiculo_data.items():
        if hasattr(veiculo, key):
            setattr(veiculo, key, value)
    session.commit()
    session.refresh(veiculo)
    return veiculo

def delete_veiculo(session: Session, veiculo_id: int) -> bool:
    veiculo = session.query(Veiculo).filter(Veiculo.id == veiculo_id).first()
    if not veiculo:
        return False
    session.delete(veiculo)
    session.commit()
    return True
