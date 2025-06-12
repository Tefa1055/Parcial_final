from typing import List, Optional
from datetime import datetime
from sqlmodel import Field, SQLModel, Relationship
from pydantic import BaseModel

# Modelo base para los usuarios
class UsuarioBase(SQLModel):
    title: str = Field(index=True)
    developer: Optional[str] = None
    release_year: Optional[int] = None

# Modelo de tabla para los juegos (para la base de datos)
class Usuario(UsuarioBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
