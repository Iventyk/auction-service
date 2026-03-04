from datetime import datetime
from decimal import Decimal
from enum import Enum

from sqlalchemy import DateTime, Enum as SqlEnum, Numeric, String, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.base import Base


class LotStatus(str, Enum):
    RUNNING = "running"
    ENDED = "ended"


class Lot(Base):
    __tablename__ = "lots"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    title: Mapped[str] = mapped_column(String(255), nullable=False)

    start_price: Mapped[Decimal] = mapped_column(
        Numeric(10, 2), nullable=False
    )

    current_price: Mapped[Decimal] = mapped_column(
        Numeric(10, 2), nullable=False
    )

    status: Mapped[LotStatus] = mapped_column(
        SqlEnum(LotStatus),
        default=LotStatus.RUNNING,
        nullable=False,
    )

    end_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    bids = relationship(
        "Bid",
        back_populates="lot",
        cascade="all, delete-orphan",
    )


class Bid(Base):
    __tablename__ = "bids"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    lot_id: Mapped[int] = mapped_column(
        ForeignKey("lots.id", ondelete="CASCADE"),
        nullable=False,
    )

    bidder_id: Mapped[str] = mapped_column(String(64), nullable=False)

    bidder_name: Mapped[str] = mapped_column(String(255), nullable=False)

    amount: Mapped[Decimal] = mapped_column(
        Numeric(10, 2), nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    lot = relationship("Lot", back_populates="bids")
