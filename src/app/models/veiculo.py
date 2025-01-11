from typing import Optional

from sqlmodel import SQLModel, Field


class Veiculo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, index=True, nullable=False)
    modelo: str = Field(max_length=100, nullable=False)
    marca: str = Field(max_length=100, nullable=False)
    placa: str = Field(max_length=7, nullable=False, unique=True)
    ano: int = Field(nullable=False)

    class Config:
        orm_mode = True