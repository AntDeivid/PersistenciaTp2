from sqlalchemy.orm import Session
from typing import List, Optional
from src.app.models.pagamento import Pagamento

def create_pagamento(session: Session, pagamento: Pagamento) -> Pagamento:
    session.add(pagamento)
    session.commit()
    session.refresh(pagamento)
    return pagamento

def get_pagamentos(session: Session) -> List[Pagamento]:
    return session.query(Pagamento).all()

def get_pagamento_by_id(session: Session, pagamento_id: int) -> Optional[Pagamento]:
    return session.query(Pagamento).filter(Pagamento.id == pagamento_id).first()

def update_pagamento(session: Session, pagamento_id: int, pagamento_data: dict) -> Optional[Pagamento]:
    pagamento = session.query(Pagamento).filter(Pagamento.id == pagamento_id).first()
    if not pagamento:
        return None
    for key, value in pagamento_data.items():
        if hasattr(pagamento, key):
            setattr(pagamento, key, value)
    session.commit()
    session.refresh(pagamento)
    return pagamento

def delete_pagamento(session: Session, pagamento_id: int) -> bool:
    pagamento = session.query(Pagamento).filter(Pagamento.id == pagamento_id).first()
    if not pagamento:
        return False
    session.delete(pagamento)
    session.commit()
    return True
