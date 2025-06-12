from typing import List, Optional
from datetime import datetime
from sqlmodel import Field, SQLModel, Relationship
from pydantic import BaseModel

# Modelo base para los usuarios
class UsuarioBase(SQLModel):
    Nombre: str = Field(index=True)
    id: int = Field(index=True)

# Modelo de tabla para los usuarios (para la base de datos)
class Usuario(UsuarioBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

class Mascota(SQLModel):
    Nombre:str = Field(..., min_length=3, max_length=20)
    id_Mascota: int = Field(default=None, primary_key=True)
