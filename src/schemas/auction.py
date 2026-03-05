from datetime import datetime, timezone
from decimal import Decimal
from enum import Enum

from pydantic import BaseModel, ConfigDict, field_validator


class LotStatus(str, Enum):
    RUNNING = "running"
    ENDED = "ended"


class LotCreate(BaseModel):
    title: str
    start_price: Decimal
    end_time: datetime

    @field_validator("end_time")
    @classmethod
    def validate_end_time(cls, value: datetime) -> datetime:
        if value.tzinfo is None:
            value = value.replace(tzinfo=timezone.utc)
        if value <= datetime.now(timezone.utc):
            raise ValueError("end_time must be in the future")

        return value


class LotRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    start_price: Decimal
    current_price: Decimal
    status: LotStatus
    end_time: datetime
    created_at: datetime


class BidCreate(BaseModel):
    bidder: str
    amount: Decimal


class BidRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    lot_id: int
    bidder_name: str
    amount: Decimal
    created_at: datetime


class BidPlaced(BaseModel):
    type: str
    lot_id: int
    bidder: str
    amount: Decimal


class TimeExtended(BaseModel):
    type: str
    lot_id: int
    end_time: datetime
