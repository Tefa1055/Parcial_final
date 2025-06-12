from datetime import datetime, timedelta
from database import SessionLocal, engine
from models import Base, User, Pet, Flight
import schemas
import crud


def init_database():
    """Initialize database with sample data"""


# Create all tables
Base.metadata.create_all(bind=engine)

db = SessionLocal()

try:

    users_data = [
        {"nombre": "Juan Pérez", "email": "juan@example.com", "telefono": "+1234567890"},
        {"nombre": "María García", "email": "maria@example.com", "telefono": "+0987654321"},
        {"nombre": "Carlos López", "email": "carlos@example.com", "telefono": "+1122334455"}
    ]

    created_users = []
    for user_data in users_data:

        existing_user = crud.get_user_by_email(db, user_data["email"])
        if not existing_user:
            user_schema = schemas.UserCreate(**user_data)
            user = crud.create_user(db, user_schema)
            created_users.append(user)
            print(f"Created user: {user.nombre} (ID: {user.id})")
        else:
            created_users.append(existing_user)
            print(f"User already exists: {existing_user.nombre} (ID: {existing_user.id})")

    pets_data = [
        {"id_usuario": created_users[0].id, "nombre_mascota": "Max", "especie": "perro", "raza": "Golden Retriever",
         "peso": 25.5, "edad": 3},
        {"id_usuario": created_users[0].id, "nombre_mascota": "Luna", "especie": "gato", "raza": "Siamés", "peso": 4.2,
         "edad": 2},
        {"id_usuario": created_users[1].id, "nombre_mascota": "Rocky", "especie": "perro", "raza": "Bulldog",
         "peso": 18.0, "edad": 5},
        {"id_usuario": created_users[2].id, "nombre_mascota": "Mimi", "especie": "gato", "raza": "Persa", "peso": 3.8,
         "edad": 1}
    ]

    for pet_data in pets_data:
        pet_schema = schemas.PetCreate(**pet_data)
        pet = crud.create_pet(db, pet_schema)
        print(f"Created pet: {pet.nombre_mascota} (ID: {pet.id}) - Owner: {pet.id_usuario}")

    base_date = datetime.now() + timedelta(days=7)  # Flights starting next week

    flights_data = [
        {
            "numero_vuelo": "HB001",
            "origen": "Madrid",
            "destino": "Barcelona",
            "fecha_salida": base_date,
            "fecha_llegada": base_date + timedelta(hours=1, minutes=30),
            "precio_base": 150.0,
            "precio_mascota": 50.0,
            "capacidad_total": 180,
            "capacidad_mascotas": 10
        },
        {
            "numero_vuelo": "HB002",
            "origen": "Barcelona",
            "destino": "Valencia",
            "fecha_salida": base_date + timedelta(days=1),
            "fecha_llegada": base_date + timedelta(days=1, hours=1),
            "precio_base": 120.0,
            "precio_mascota": 40.0,
            "capacidad_total": 150,
            "capacidad_mascotas": 8
        },
        {
            "numero_vuelo": "HB003",
            "origen": "Madrid",
            "destino": "Sevilla",
            "fecha_salida": base_date + timedelta(days=2),
            "fecha_llegada": base_date + timedelta(days=2, hours=1, minutes=15),
            "precio_base": 180.0,
            "precio_mascota": 60.0,
            "capacidad_total": 200,
            "capacidad_mascotas": 12
        },
        {
            "numero_vuelo": "HB004",
            "origen": "Valencia",
            "destino": "Madrid",
            "fecha_salida": base_date + timedelta(days=3),
            "fecha_llegada": base_date + timedelta(days=3, hours=1, minutes=20),
            "precio_base": 140.0,
            "precio_mascota": 45.0,
            "capacidad_total": 160,
            "capacidad_mascotas": 9
        }
    ]

    for flight_data in flights_data:
        flight_schema = schemas.FlightCreate(**flight_data)
        flight = crud.create_flight(db, flight_schema)
        print(f"Created flight: {flight.numero_vuelo} - {flight.origen} to {flight.destino} (ID: {flight.id})")

    print("\n✅ Database initialized successfully!")
    print("\n📋 Summary:")
    print(f"- Users created: {len(created_users)}")
    print(f"- Pets created: {len(pets_data)}")
    print(f"- Flights created: {len(flights_data)}")
    print("\n🌐 You can now:")
    print("1. Visit http://localhost:8000 to use the web interface")
    print("2. Visit http://localhost:8000/docs for API documentation")
    print("3. Start making reservations!")

except Exception as e:
    print(f"❌ Error initializing database: {e}")
    db.rollback()
finally:
    db.close()
