from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class Manutencao (SQLModel, table=True): 
    id: Optional[int] = Field(default=None, primary_key=True, index=True, nullable=False)
    data: datetime = Field(nullable=False)
    tipo_manutencao: str = Field(nullable=False)
    custo : float = Field(nullable=False)
    observacao: str = Field(nullable=False)

    class Config:
        orm_mode = True
