from sqlalchemy.orm import Session
from sqlalchemy import and_, func
from datetime import datetime, date
import models
import schemas
import random
import string

def get_user(db: Session, user_id: int):
return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
return db.query(models.User).filter(models.User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
db_user = models.User(**user.dict())
db.add(db_user)
db.commit()
db.refresh(db_user)
return db_user

def update_user(db: Session, user_id: int, user: schemas.UserUpdate):
db_user = db.query(models.User).filter(models.User.id == user_id).first()
if db_user:
update_data = user.dict(exclude_unset=True)
for field, value in update_data.items():
setattr(db_user, field, value)
db.commit()
db.refresh(db_user)
return db_user

def delete_user(db: Session, user_id: int):
db_user = db.query(models.User).filter(models.User.id == user_id).first()
if db_user:
db.delete(db_user)
db.commit()
return db_user

def get_pet(db: Session, pet_id: int):
return db.query(models.Pet).filter(models.Pet.id == pet_id).first()

def get_pets_by_user(db: Session, user_id: int):
return db.query(models.Pet).filter(models.Pet.id_usuario == user_id).all()

def get_pets(db: Session, skip: int = 0, limit: int = 100):
return db.query(models.Pet).offset(skip).limit(limit).all()

def create_pet(db: Session, pet: schemas.PetCreate):
db_pet = models.Pet(**pet.dict())
db.add(db_pet)
db.commit()
db.refresh(db_pet)
return db_pet

def update_pet(db: Session, pet_id: int, pet: schemas.PetUpdate):
db_pet = db.query(models.Pet).filter(models.Pet.id == pet_id).first()
if db_pet:
update_data = pet.dict(exclude_unset=True)
for field, value in update_data.items():
setattr(db_pet, field, value)
db.commit()
db.refresh(db_pet)
return db_pet

def delete_pet(db: Session, pet_id: int):
db_pet = db.query(models.Pet).filter(models.Pet.id == pet_id).first()
if db_pet:
db.delete(db_pet)
db.commit()
return db_pet