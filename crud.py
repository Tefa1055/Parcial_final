from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import List, Optional
from datetime import date
import random
import string

from models import Usuario, Mascota, Vuelo, Reserva
from schemas import UsuarioCreate, MascotaCreate, ReservaCreate
from auth import hash_password

def crear_usuario(db: Session, usuario: UsuarioCreate) -> Usuario:
    password_hash = hash_password(usuario.password)
    db_usuario = Usuario(
        nombre=usuario.nombre,
        apellido=usuario.apellido,
        email=usuario.email,
        telefono=usuario.telefono,
        password_hash=password_hash
    )
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

def obtener_usuario_por_email(db: Session, email: str) -> Optional[Usuario]:
    return db.query(Usuario).filter(Usuario.email == email).first()

def obtener_usuario_por_id(db: Session, usuario_id: int) -> Optional[Usuario]:
    return db.query(Usuario).filter(Usuario.id == usuario_id).first()

def crear_mascota(db: Session, mascota: MascotaCreate, propietario_id: int) -> Mascota:
    db_mascota = Mascota(
        nombre=mascota.nombre,
        especie=mascota.especie,
        raza=mascota.raza,
        edad=mascota.edad,
        peso=mascota.peso,
        observaciones=mascota.observaciones,
        propietario_id=propietario_id
    )
    db.add(db_mascota)
    db.commit()
    db.refresh(db_mascota)
    return db_mascota

def obtener_mascotas_usuario(db: Session, usuario_id: int) -> List[Mascota]:
    return db.query(Mascota).filter(
        and_(Mascota.propietario_id == usuario_id, Mascota.activo == True)
    ).all()

def obtener_mascota_por_id(db: Session, mascota_id: int) -> Optional[Mascota]:
    return db.query(Mascota).filter(Mascota.id == mascota_id).first()
    
def buscar_vuelos(db: Session, origen: str, destino: str, fecha: date) -> List[Vuelo]:
    return db.query(Vuelo).filter(
        and_(
            Vuelo.origen.ilike(f"%{origen}%"),
            Vuelo.destino.ilike(f"%{destino}%"),
            Vuelo.fecha_salida == fecha,
            Vuelo.disponible == True
        )
    ).all()

def obtener_vuelo_por_id(db: Session, vuelo_id: int) -> Optional[Vuelo]:
    return db.query(Vuelo).filter(Vuelo.id == vuelo_id).first()

def verificar_disponibilidad_vuelo(db: Session, vuelo_id: int) -> bool:
    vuelo = obtener_vuelo_por_id(db, vuelo_id)
    if not vuelo or not vuelo.disponible:
        return False
    
    # Contar reservas activas para este vuelo
    reservas_activas = db.query(Reserva).filter(
        and_(
            Reserva.vuelo_id == vuelo_id,
            Reserva.estado == "confirmada"
        )
    ).count()
    
    return reservas_activas < vuelo.capacidad_mascotas

def generar_codigo_reserva() -> str:
    """Genera un código de reserva único de 8 caracteres"""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

def crear_reserva(db: Session, reserva: ReservaCreate, usuario_id: int) -> Reserva:
    # Verificar que el vuelo existe y está disponible
    vuelo = obtener_vuelo_por_id(db, reserva.vuelo_id)
    if not vuelo:
        raise ValueError("Vuelo no encontrado")
    
    if not verificar_disponibilidad_vuelo(db, reserva.vuelo_id):
        raise ValueError("Vuelo no disponible")
    
    # Verificar que la mascota pertenece al usuario
    mascota = obtener_mascota_por_id(db, reserva.mascota_id)
    if not mascota or mascota.propietario_id != usuario_id:
        raise ValueError("Mascota no encontrada o no pertenece al usuario")
    
    # Calcular precio total
    precio_total = vuelo.precio_base + vuelo.precio_mascota
    
    # Generar código de reserva único
    codigo_reserva = generar_codigo_reserva()
    while db.query(Reserva).filter(Reserva.codigo_reserva == codigo_reserva).first():
        codigo_reserva = generar_codigo_reserva()
    
    db_reserva = Reserva(
        codigo_reserva=codigo_reserva,
        usuario_id=usuario_id,
        vuelo_id=reserva.vuelo_id,
        mascota_id=reserva.mascota_id,
        precio_total=precio_total,
        observaciones=reserva.observaciones
    )
    
    db.add(db_reserva)
    db.commit()
    db.refresh(db_reserva)
    return db_reserva

def obtener_reservas_usuario(db: Session, usuario_id: int) -> List[Reserva]:
    return db.query(Reserva).filter(Reserva.usuario_id == usuario_id).all()

def obtener_reserva_por_codigo(db: Session, codigo_reserva: str) -> Optional[Reserva]:
    return db.query(Reserva).filter(Reserva.codigo_reserva == codigo_reserva).first()

def verificar_password(password: str, password_hash: str) -> bool:
    from auth import verify_password
    return verify_password(password, password_hash)
