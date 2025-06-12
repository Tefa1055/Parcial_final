from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

    class User(Base):
        tablename = "users"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    telefono = Column(String(20))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    mascotas = relationship("Pet", back_populates="owner")
    reservas = relationship("Reservation", back_populates="user")

    class Pet(Base):
        tablename = "pets"

        id = Column(Integer, primary_key=True, index=True)
        id_usuario = Column(Integer, ForeignKey("users.id"), nullable=False)
        nombre_mascota = Column(String(100), nullable=False)
        especie = Column(String(50), nullable=False)  #perro, gato, etc.
        raza = Column(String(100))
        peso = Column(Float, nullable=False)  # en kg
        edad = Column(Integer)
        observaciones = Column(Text)
        created_at = Column(DateTime(timezone=True), server_default=func.now())

    owner = relationship("User", back_populates="mascotas")

    class Flight(Base):
    tablename = "flights"

    id = Column(Integer, primary_key=True, index=True)
    numero_vuelo = Column(String(10), unique=True, nullable=False)
    origen = Column(String(100), nullable=False)
    destino = Column(String(100), nullable=False)
    fecha_salida = Column(DateTime, nullable=False)
    fecha_llegada = Column(DateTime, nullable=False)
    precio_base = Column(Float, nullable=False)
    precio_mascota = Column(Float, nullable=False)
    capacidad_total = Column(Integer, nullable=False)
    capacidad_mascotas = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

reservas = relationship("Reservation", back_populates="flight")

class Reservation(Base):
tablename = "reservations"

id = Column(Integer, primary_key=True, index=True)
id_usuario = Column(Integer, ForeignKey("users.id"), nullable=False)
id_vuelo = Column(Integer, ForeignKey("flights.id"), nullable=False)
id_mascota = Column(Integer, ForeignKey("pets.id"), nullable=False)
codigo_reserva = Column(String(20), unique=True, nullable=False)
estado = Column(String(20), default="pendiente")  # pendiente, confirmada, cancelada
precio_total = Column(Float, nullable=False)
fecha_reserva = Column(DateTime(timezone=True), server_default=func.now())

user = relationship("User", back_populates="reservas")
flight = relationship("Flight", back_populates="reservas")
pet = relationship("Pet")
compra = relationship("Purchase", back_populates="reservation", uselist=False)

class Purchase(Base):
tablename = "purchases"

id = Column(Integer, primary_key=True, index=True)
id_reserva = Column(Integer, ForeignKey("reservations.id"), nullable=False)
metodo_pago = Column(String(50), nullable=False)  # tarjeta, transferencia, etc.
estado_pago = Column(String(20), default="pendiente")  # pendiente, completado, fallido
monto = Column(Float, nullable=False)
fecha_compra = Column(DateTime(timezone=True), server_default=func.now())
referencia_pago = Column(String(100))

reservation = relationship("Reservation", back_populates="compra")
