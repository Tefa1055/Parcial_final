from sqlalchemy import Column, Integer, String, DateTime, Date, Float, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class Usuario(Base):
    __tablename__ = "usuarios"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    apellido = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    telefono = Column(String(20), nullable=False)
    password_hash = Column(String(255), nullable=False)
    fecha_registro = Column(DateTime(timezone=True), server_default=func.now())
    activo = Column(Boolean, default=True)
    
    # Relaciones
    mascotas = relationship("Mascota", back_populates="propietario")
    reservas = relationship("Reserva", back_populates="usuario")

class Mascota(Base):
    __tablename__ = "mascotas"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    especie = Column(String(50), nullable=False)  # perro, gato, etc.
    raza = Column(String(100))
    edad = Column(Integer)
    peso = Column(Float, nullable=False)  # en kg
    observaciones = Column(Text)
    propietario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    fecha_registro = Column(DateTime(timezone=True), server_default=func.now())
    activo = Column(Boolean, default=True)
    
    # Relaciones
    propietario = relationship("Usuario", back_populates="mascotas")
    reservas = relationship("Reserva", back_populates="mascota")

class Vuelo(Base):
    __tablename__ = "vuelos"
    
    id = Column(Integer, primary_key=True, index=True)
    numero_vuelo = Column(String(10), unique=True, nullable=False)
    origen = Column(String(100), nullable=False)
    destino = Column(String(100), nullable=False)
    fecha_salida = Column(Date, nullable=False)
    hora_salida = Column(String(5), nullable=False)  # HH:MM
    fecha_llegada = Column(Date, nullable=False)
    hora_llegada = Column(String(5), nullable=False)  # HH:MM
    precio_base = Column(Float, nullable=False)
    precio_mascota = Column(Float, nullable=False)
    capacidad_total = Column(Integer, nullable=False)
    capacidad_mascotas = Column(Integer, nullable=False)
    disponible = Column(Boolean, default=True)
    
    # Relaciones
    reservas = relationship("Reserva", back_populates="vuelo")

class Reserva(Base):
    __tablename__ = "reservas"
    
    id = Column(Integer, primary_key=True, index=True)
    codigo_reserva = Column(String(10), unique=True, nullable=False)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    vuelo_id = Column(Integer, ForeignKey("vuelos.id"), nullable=False)
    mascota_id = Column(Integer, ForeignKey("mascotas.id"), nullable=False)
    precio_total = Column(Float, nullable=False)
    estado = Column(String(20), default="confirmada")  # confirmada, cancelada, completada
    fecha_reserva = Column(DateTime(timezone=True), server_default=func.now())
    observaciones = Column(Text)
    
    # Relaciones
    usuario = relationship("Usuario", back_populates="reservas")
    vuelo = relationship("Vuelo", back_populates="reservas")
    mascota = relationship("Mascota", back_populates="reservas")
