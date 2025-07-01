"""Script to insert sample vehicle data into MongoDB."""

import asyncio
from datetime import datetime

from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URI = "mongodb://localhost:27017"  # Replace with your MongoDB URI
DB_NAME = "vehicle_history"


async def main():
    client = AsyncIOMotorClient(MONGO_URI)
    db = client[DB_NAME]

    vehicle = {
        "rc_number": "MH12AB1234",
        "owner_name": "Rahul",
        "model": "Swift",
        "make": "Maruti",
        "fuel_type": "Petrol",
        "year": 2018,
        "registration_date": "2018-05-20",
        "insurance_status": "Active",
        "challan_history": [
            {"date": "2022-01-15", "offense": "Speeding", "amount": 500}
        ],
        "service_history": [
            {
                "date": "2023-03-10",
                "service_type": "Oil Change",
                "notes": "Regular service",
            }
        ],
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
    }

    await db["vehicles"].insert_one(vehicle)
    print("Inserted sample vehicle")
    client.close()


if __name__ == "__main__":
    asyncio.run(main())
