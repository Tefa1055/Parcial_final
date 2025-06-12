from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from typing import List
import os

from database import SessionLocal, engine, get_db
from models import Base, User, Pet, Flight, Reservation, Purchase
import schemas
import crud

Base.metadata.create_all(bind=engine)

app = FastAPI(
title="Hablar - Airline Pet Travel System",
description="Sistema de reservas de vuelos para mascotas",
version="1.0.0"
)

templates = Jinja2Templates(directory="templates")

if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
if db_user:
    raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
if db_user is None:
    raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.put("/users/{user_id}", response_model=schemas.User)
def update_user(user_id: int, user: schemas.UserUpdate, db: Session = Depends(get_db)):
    db_user = crud.update_user(db, user_id=user_id, user=user)
if db_user is None:
    raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    success = crud.delete_user(db, user_id=user_id)
if not success:
    raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}

@app.post("/pets/", response_model=schemas.Pet)
def create_pet(pet: schemas.PetCreate, db: Session = Depends(get_db)):
    return crud.create_pet(db=db, pet=pet)

@app.get("/pets/", response_model=List[schemas.Pet])
def read_pets(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    pets = crud.get_pets(db, skip=skip, limit=limit)
    return pets

@app.get("/pets/{pet_id}", response_model=schemas.Pet)
def read_pet(pet_id: int, db: Session = Depends(get_db)):
    db_pet = crud.get_pet(db, pet_id=pet_id)
if db_pet is None:
    raise HTTPException(status_code=404, detail="Pet not found")
    return db_pet

@app.get("/users/{user_id}/pets/", response_model=List[schemas.Pet])
def read_user_pets(user_id: int, db: Session = Depends(get_db)):
    pets = crud.get_pets_by_user(db, user_id=user_id)
    return pets

@app.put("/pets/{pet_id}", response_model=schemas.Pet)
def update_pet(pet_id: int, pet: schemas.PetUpdate, db: Session = Depends(get_db)):
    db_pet = crud.update_pet(db, pet_id=pet_id, pet=pet)
if db_pet is None:
    raise HTTPException(status_code=404, detail="Pet not found")
    return db_pet

@app.delete("/pets/{pet_id}")
def delete_pet(pet_id: int, db: Session = Depends(get_db)):
    success = crud.delete_pet(db, pet_id=pet_id)
if not success:
    raise HTTPException(status_code=404, detail="Pet not found")
    return {"message": "Pet deleted successfully"}

@app.post("/flights/", response_model=schemas.Flight)
def create_flight(flight: schemas.FlightCreate, db: Session = Depends(get_db)):
    return crud.create_flight(db=db, flight=flight)

@app.get("/flights/", response_model=List[schemas.Flight])
def read_flights(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    flights = crud.get_flights(db, skip=skip, limit=limit)
    return flights

@app.get("/flights/{flight_id}", response_model=schemas.Flight)
def read_flight(flight_id: int, db: Session = Depends(get_db)):
    db_flight = crud.get_flight(db, flight_id=flight_id)
if db_flight is None:
    raise HTTPException(status_code=404, detail="Flight not found")
    return db_flight

@app.post("/flights/search/", response_model=List[schemas.Flight])
def search_flights(search: schemas.FlightSearch, db: Session = Depends(get_db)):
    flights = crud.search_flights(db, search.origen, search.destino, search.fecha)
    return flights

@app.put("/flights/{flight_id}", response_model=schemas.Flight)
def update_flight(flight_id: int, flight: schemas.FlightUpdate, db: Session = Depends(get_db)):
    db_flight = crud.update_flight(db, flight_id=flight_id, flight=flight)
if db_flight is None:
    raise HTTPException(status_code=404, detail="Flight not found")
    return db_flight

@app.delete("/flights/{flight_id}")
def delete_flight(flight_id: int, db: Session = Depends(get_db)):
    success = crud.delete_flight(db, flight_id=flight_id)
if not success:
    raise HTTPException(status_code=404, detail="Flight not found")
    return {"message": "Flight deleted successfully"}

@app.post("/reservations/", response_model=schemas.Reservation)
def create_reservation(reservation: schemas.ReservationCreate, db: Session = Depends(get_db)):
    return crud.create_reservation(db=db, reservation=reservation)

@app.get("/reservations/", response_model=List[schemas.Reservation])
def read_reservations(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    reservations = crud.get_reservations(db, skip=skip, limit=limit)
    return reservations

@app.get("/reservations/{reservation_id}", response_model=schemas.Reservation)
def read_reservation(reservation_id: int, db: Session = Depends(get_db)):
    db_reservation = crud.get_reservation(db, reservation_id=reservation_id)
if db_reservation is None:
    raise HTTPException(status_code=404, detail="Reservation not found")
    return db_reservation

@app.get("/users/{user_id}/reservations/", response_model=List[schemas.Reservation])
def read_user_reservations(user_id: int, db: Session = Depends(get_db)):
    reservations = crud.get_reservations_by_user(db, user_id=user_id)
    return reservations

@app.put("/reservations/{reservation_id}", response_model=schemas.Reservation)
def update_reservation(reservation_id: int, reservation: schemas.ReservationUpdate, db: Session = Depends(get_db)):
    db_reservation = crud.update_reservation(db, reservation_id=reservation_id, reservation=reservation)
if db_reservation is None:
    raise HTTPException(status_code=404, detail="Reservation not found")
    return db_reservation

@app.delete("/reservations/{reservation_id}")
def delete_reservation(reservation_id: int, db: Session = Depends(get_db)):
    success = crud.delete_reservation(db, reservation_id=reservation_id)
if not success:
    raise HTTPException(status_code=404, detail="Reservation not found")
    return {"message": "Reservation deleted successfully"}

@app.post("/purchases/", response_model=schemas.Purchase)
def create_purchase(purchase: schemas.PurchaseCreate, db: Session = Depends(get_db)):
    return crud.create_purchase(db=db, purchase=purchase)

@app.get("/purchases/", response_model=List[schemas.Purchase])
def read_purchases(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    purchases = crud.get_purchases(db, skip=skip, limit=limit)
    return purchases

@app.get("/purchases/{purchase_id}", response_model=schemas.Purchase)
def read_purchase(purchase_id: int, db: Session = Depends(get_db)):
    db_purchase = crud.get_purchase(db, purchase_id=purchase_id)
if db_purchase is None:
    raise HTTPException(status_code=404, detail="Purchase not found")
    return db_purchase

@app.put("/purchases/{purchase_id}", response_model=schemas.Purchase)
def update_purchase(purchase_id: int, purchase: schemas.PurchaseUpdate, db: Session = Depends(get_db)):
    db_purchase = crud.update_purchase(db, purchase_id=purchase_id, purchase=purchase)
if db_purchase is None:
    raise HTTPException(status_code=404, detail="Purchase not found")
    return db_purchase