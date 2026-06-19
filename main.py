from fastapi import FastAPI, HTTPException, Depends, status
from database import engine, SessionLocal, Base
from models import Vehicle
from auth import create_token
from schemas import *
from fastapi.security import OAuth2PasswordRequestForm
from auth import *


app = FastAPI()

Base.metadata.create_all(bind=engine)

db = SessionLocal()

# # Login
# @app.post("/login")
# def login():
#     token = create_token("admin")
#     return {"token": token}

@app.post('/login', summary="Create access and refresh tokens for user", response_model=TokenSchema)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = db.get(form_data.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User not found!"
        )

    hashed_pass = user['password']
    if not verify_password(form_data.password, hashed_pass):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )

    return {
        "access_token": create_access_token(user['email']),
        "refresh_token": create_refresh_token(user['email']),
    }

# Create
@app.post("/vehicle")
def add_vehicle(number: str, owner: str, model: str):
    vehicle = Vehicle(
        number=number,
        owner=owner,
        model=model
    )
    db.add(vehicle)
    db.commit()
    return {"message": "Vehicle Added"}

# Read
@app.get("/vehicles")
def get_vehicles():
    return db.query(Vehicle).all()

# # Update
# @app.put("/vehicle/{id}")
# def update_vehicle(id: int, owner: str):
#     vehicle = db.query(Vehicle).filter(
#         Vehicle.id == id
#     ).first()

#     vehicle.owner = owner
#     db.commit()

#     return {"message": "Updated"}

# # Delete
# @app.delete("/vehicle/{id}")
# def delete_vehicle(id: int):
#     vehicle = db.query(Vehicle).filter(
#         Vehicle.id == id
#     ).first()

#     db.delete(vehicle)
#     db.commit()

#     return {"message": "Deleted"}