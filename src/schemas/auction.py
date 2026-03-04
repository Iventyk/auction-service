from datetime import datetime
from decimal import Decimal
from enum import Enum

from pydantic import BaseModel, ConfigDict, field_validator


class LotStatus(str, Enum):
    RUNNING = "running"
    ENDED = "ended"


class LotBase(BaseModel):
    title: str
    start_price: Decimal
    end_time: datetime

    @field_validator("end_time")
    @classmethod
    def validate_end_time(cls, v: datetime) -> datetime:
        if v <= datetime.now():
            raise ValueError("end_time must be in the future")
        return v


class LotCreate(LotBase):
    pass


class LotRead(LotBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    current_price: Decimal
    status: LotStatus
    created_at: datetime


class BidBase(BaseModel):
    bidder_id: str
    bidder_name: str
    amount: Decimal


class BidCreate(BidBase):
    pass


class BidRead(BidBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    lot_id: int
    created_at: datetime
