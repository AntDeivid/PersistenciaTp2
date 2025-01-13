from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from src.app.models.usuario import Usuario
from typing import List, Optional

def create_usuario(session: Session, usuario: Usuario) -> Usuario:
    session.add(usuario)
    try:
        session.commit()
        session.refresh(usuario)
        return usuario
    except IntegrityError:
        session.rollback()
        raise ValueError("Email ou CPF já cadastrados!")

def get_usuarios(session: Session) -> List[Usuario]:
    return session.query(Usuario).all()

def get_usuario_by_id(session: Session, usuario_id: int) -> Optional[Usuario]:
    return session.query(Usuario).filter(Usuario.id == usuario_id).first()

def update_usuario(session: Session, usuario_id: int, usuario_data: dict) -> Optional[Usuario]:
    usuario = session.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        return None
    for key, value in usuario_data.items():
        if hasattr(usuario, key):
            setattr(usuario, key, value)
    session.commit()
    session.refresh(usuario)
    return usuario

def delete_usuario(session: Session, usuario_id: int) -> bool:
    usuario = session.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        return False
    session.delete(usuario)
    session.commit()
    return True
