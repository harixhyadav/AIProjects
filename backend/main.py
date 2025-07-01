from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorDatabase
from pymongo.errors import PyMongoError

from .database import init_db
from .models import CheckVehicleRequest, VehicleResponse

MONGO_URI = "mongodb://localhost:27017"  # Replace with actual MongoDB URI
DB_NAME = "vehicle_history"

app = FastAPI(title="Vehicle History API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

mongodb = init_db(app, MONGO_URI, DB_NAME)


def get_db() -> AsyncIOMotorDatabase:
    return mongodb.db


@app.post("/vehicle/check", response_model=VehicleResponse)
async def check_vehicle(
    payload: CheckVehicleRequest, db: AsyncIOMotorDatabase = Depends(get_db)
):
    rc_number = payload.rc_number.strip().upper()
    if not rc_number:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid RC number",
        )

    try:
        document = await db["vehicles"].find_one(
            {"rc_number": rc_number}, {"_id": 0}
        )
    except PyMongoError:
        raise HTTPException(status_code=500, detail="Database connection error")

    if not document:
        raise HTTPException(status_code=404, detail="Vehicle not found")

    return VehicleResponse(**document)
