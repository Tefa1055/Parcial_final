from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime, date

class UsuarioBase(BaseModel):
    nombre: str
    apellido: str
    email: EmailStr
    telefono: str

class UsuarioCreate(UsuarioBase):
    password: str

class UsuarioLogin(BaseModel):
    email: EmailStr
    password: str

class UsuarioResponse(UsuarioBase):
    id: int
    fecha_registro: datetime
    activo: bool
    
    class Config:
        from_attributes = True

class MascotaBase(BaseModel):
    nombre: str
    especie: str
    raza: Optional[str] = None
    edad: Optional[int] = None
    peso: float
    observaciones: Optional[str] = None

class MascotaCreate(MascotaBase):
    pass

class MascotaResponse(MascotaBase):
    id: int
    propietario_id: int
    fecha_registro: datetime
    activo: bool
    
    class Config:
        from_attributes = True

class VueloBase(BaseModel):
    numero_vuelo: str
    origen: str
    destino: str
    fecha_salida: date
    hora_salida: str
    fecha_llegada: date
    hora_llegada: str
    precio_base: float
    precio_mascota: float

class VueloResponse(VueloBase):
    id: int
    capacidad_total: int
    capacidad_mascotas: int
    disponible: bool
    
    class Config:
        from_attributes = True

class VueloSearch(BaseModel):
    origen: str
    destino: str
    fecha: date

class ReservaBase(BaseModel):
    vuelo_id: int
    mascota_id: int
    observaciones: Optional[str] = None

class ReservaCreate(ReservaBase):
    pass

class ReservaResponse(ReservaBase):
    id: int
    codigo_reserva: str
    usuario_id: int
    precio_total: float
    estado: str
    fecha_reserva: datetime
    vuelo: VueloResponse
    mascota: MascotaResponse
    
    class Config:
        from_attributes = True
