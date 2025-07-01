from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import FastAPI
from typing import Optional

class MongoDB:
    def __init__(self, uri: str, db_name: str):
        self._client: Optional[AsyncIOMotorClient] = None
        self.uri = uri
        self.db_name = db_name

    async def connect(self):
        self._client = AsyncIOMotorClient(self.uri)

    async def close(self):
        if self._client:
            self._client.close()

    @property
    def client(self) -> AsyncIOMotorClient:
        if not self._client:
            raise RuntimeError("MongoDB client is not initialized")
        return self._client

    @property
    def db(self):
        return self.client[self.db_name]

def init_db(app: FastAPI, uri: str, db_name: str) -> MongoDB:
    mongodb = MongoDB(uri, db_name)

    @app.on_event("startup")
    async def startup():
        await mongodb.connect()

    @app.on_event("shutdown")
    async def shutdown():
        await mongodb.close()

    return mongodb
