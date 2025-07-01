from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field, validator


def mask_owner_name(name: str) -> str:
    if not name:
        return ""
    first_letter = name[0]
    return first_letter + "*" * (len(name) - 1)


class ChallanEntry(BaseModel):
    date: str
    offense: str
    amount: int


class ServiceEntry(BaseModel):
    date: str
    service_type: str
    notes: str


class CheckVehicleRequest(BaseModel):
    rc_number: str = Field(..., alias="rc_number")

    @validator("rc_number")
    def validate_rc_number(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("RC number must not be empty")
        return v.strip().upper()


class VehicleResponse(BaseModel):
    rc_number: str
    owner_name: str
    model: str
    make: str
    fuel_type: str
    year: int
    registration_date: str
    insurance_status: str
    challan_history: List[ChallanEntry]
    service_history: List[ServiceEntry]
    created_at: datetime
    updated_at: datetime

    @validator("owner_name", pre=True)
    def mask_owner(cls, v: str) -> str:
        return mask_owner_name(v)
