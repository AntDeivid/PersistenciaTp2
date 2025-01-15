import logging
from sqlite3 import IntegrityError
from typing import Optional

from src.app.core.db.database import get_db
from src.app.models.usuario import Usuario


class UsuarioRepository:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def create(self, usuario: Usuario) -> Usuario:
        try:
            with next(get_db()) as db:
                db.add(usuario)
                db.commit()
                db.refresh(usuario)
                return usuario
        except IntegrityError:
            self.logger.error("Erro ao criar usuário!")
            raise ValueError("Erro ao criar usuário!")

    def get_all_no_pagination(self) -> list[Usuario]:
        with next(get_db()) as db:
            return db.query(Usuario).all()

    def get_all(self, page: Optional[int] = 1, limit: Optional[int] = 10) -> list[Usuario]:
        with next(get_db()) as db:
            return db.query(Usuario).offset((page - 1) * limit).limit(limit).all()

    def get_by_id(self, usuario_id: int) -> Usuario:
        with next(get_db()) as db:
            return db.query(Usuario).filter(Usuario.id == usuario_id).first()

    def get_quantidade_usuarios(self) -> int:
        with next(get_db()) as db:
            return db.query(Usuario).count()

    def update(self, usuario_id: int, usuario_data: dict) -> Usuario:
        with next(get_db()) as db:
            usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
            if not usuario:
                return None
            for key, value in usuario_data.items():
                if hasattr(usuario, key):
                    setattr(usuario, key, value)
            db.commit()
            db.refresh(usuario)
            return usuario

    def delete(self, usuario_id: int) -> bool:
        with next(get_db()) as db:
            usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
            if not usuario:
                return False
            db.delete(usuario)
            db.commit()
            return True