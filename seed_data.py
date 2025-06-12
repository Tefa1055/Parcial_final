from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Base, Vuelo
from datetime import date, timedelta

Base.metadata.create_all(bind=engine)

def crear_vuelos_ejemplo():
    """Crea algunos vuelos de ejemplo para probar la aplicación"""
    db = SessionLocal()
    
    if db.query(Vuelo).first():
        print("Ya existen vuelos en la base de datos")
        db.close()
        return
    
    vuelos_ejemplo = [
        {
            "numero_vuelo": "AM001",
            "origen": "Madrid",
            "destino": "Barcelona",
            "fecha_salida": date.today() + timedelta(days=7),
            "hora_salida": "08:00",
            "fecha_llegada": date.today() + timedelta(days=7),
            "hora_llegada": "09:30",
            "precio_base": 150.0,
            "precio_mascota": 50.0,
            "capacidad_total": 180,
            "capacidad_mascotas": 20
        },
        {
            "numero_vuelo": "AM002",
            "origen": "Barcelona",
            "destino": "Madrid",
            "fecha_salida": date.today() + timedelta(days=7),
            "hora_salida": "14:00",
            "fecha_llegada": date.today() + timedelta(days=7),
            "hora_llegada": "15:30",
            "precio_base": 150.0,
            "precio_mascota": 50.0,
            "capacidad_total": 180,
            "capacidad_mascotas": 20
        },
        {
            "numero_vuelo": "AM003",
            "origen": "Madrid",
            "destino": "Sevilla",
            "fecha_salida": date.today() + timedelta(days=8),
            "hora_salida": "10:00",
            "fecha_llegada": date.today() + timedelta(days=8),
            "hora_llegada": "11:15",
            "precio_base": 120.0,
            "precio_mascota": 40.0,
            "capacidad_total": 150,
            "capacidad_mascotas": 15
        },
        {
            "numero_vuelo": "AM004",
            "origen": "Valencia",
            "destino": "Bilbao",
            "fecha_salida": date.today() + timedelta(days=9),
            "hora_salida": "16:00",
            "fecha_llegada": date.today() + timedelta(days=9),
            "hora_llegada": "17:45",
            "precio_base": 180.0,
            "precio_mascota": 60.0,
            "capacidad_total": 200,
            "capacidad_mascotas": 25
        },
        {
            "numero_vuelo": "AM005",
            "origen": "Málaga",
            "destino": "Madrid",
            "fecha_salida": date.today() + timedelta(days=10),
            "hora_salida": "12:00",
            "fecha_llegada": date.today() + timedelta(days=10),
            "hora_llegada": "13:30",
            "precio_base": 140.0,
            "precio_mascota": 45.0,
            "capacidad_total": 160,
            "capacidad_mascotas": 18
        }
    ]
    
    for vuelo_data in vuelos_ejemplo:
        vuelo = Vuelo(**vuelo_data)
        db.add(vuelo)
    
    db.commit()
    print(f"Se crearon {len(vuelos_ejemplo)} vuelos de ejemplo")
    db.close()

if __name__ == "__main__":
    crear_vuelos_ejemplo()
