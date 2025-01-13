from sqlalchemy.orm import Session
from typing import List, Optional
from src.app.models.contrato import Contrato

def create_contrato(session: Session, contrato: Contrato) -> Contrato:
    session.add(contrato)
    session.commit()
    session.refresh(contrato)
    return contrato

def get_contratos(session: Session) -> List[Contrato]:
    return session.query(Contrato).all()

def get_contrato_by_id(session: Session, contrato_id: int) -> Optional[Contrato]:
    return session.query(Contrato).filter(Contrato.id == contrato_id).first()

def update_contrato(session: Session, contrato_id: int, contrato_data: dict) -> Optional[Contrato]:
    contrato = session.query(Contrato).filter(Contrato.id == contrato_id).first()
    if not contrato:
        return None
    for key, value in contrato_data.items():
        if hasattr(contrato, key):
            setattr(contrato, key, value)
    session.commit()
    session.refresh(contrato)
    return contrato

def delete_contrato(session: Session, contrato_id: int) -> bool:
    contrato = session.query(Contrato).filter(Contrato.id == contrato_id).first()
    if not contrato:
        return False
    session.delete(contrato)
    session.commit()
    return True
