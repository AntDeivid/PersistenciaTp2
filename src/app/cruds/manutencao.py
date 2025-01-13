from sqlalchemy.orm import Session
from typing import List, Optional
from src.app.models.manutencao import Manutencao

def create_manutencao(session: Session, manutencao: Manutencao) -> Manutencao:
    session.add(manutencao)
    session.commit()
    session.refresh(manutencao)
    return manutencao

def get_manutencoes(session: Session) -> List[Manutencao]:
    return session.query(Manutencao).all()

def get_manutencao_by_id(session: Session, manutencao_id: int) -> Optional[Manutencao]:
    return session.query(Manutencao).filter(Manutencao.id == manutencao_id).first()

def update_manutencao(session: Session, manutencao_id: int, manutencao_data: dict) -> Optional[Manutencao]:
    manutencao = session.query(Manutencao).filter(Manutencao.id == manutencao_id).first()
    if not manutencao:
        return None
    for key, value in manutencao_data.items():
        if hasattr(manutencao, key):
            setattr(manutencao, key, value)
    session.commit()
    session.refresh(manutencao)
    return manutencao

def delete_manutencao(session: Session, manutencao_id: int) -> bool:
    manutencao = session.query(Manutencao).filter(Manutencao.id == manutencao_id).first()
    if not manutencao:
        return False
    session.delete(manutencao)
    session.commit()
    return True
