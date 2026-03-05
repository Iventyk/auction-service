from datetime import datetime, timedelta, timezone
from typing import cast

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models.auction import Bid, Lot, LotStatus
from src.exceptions import BidTooLowError, LotEndedError, LotNotFoundError
from src.schemas.auction import (
    BidCreate,
    BidPlaced,
    LotCreate,
    TimeExtended,
)

TIME_EXTENSION_WINDOW = timedelta(seconds=60)
TIME_EXTENSION_AMOUNT = timedelta(seconds=60)


class AuctionCrud:
    async def create_lot(
        self, session: AsyncSession, payload: LotCreate
    ) -> Lot:
        lot = Lot(
            title=payload.title,
            start_price=payload.start_price,
            current_price=payload.start_price,
            end_time=payload.end_time,
        )
        session.add(lot)
        await session.commit()
        await session.refresh(lot)
        return lot

    async def get_active_lots(self, session: AsyncSession) -> list[Lot]:
        now = datetime.now(timezone.utc)
        query = (
            select(Lot)
            .where(Lot.status == LotStatus.RUNNING)
            .where(Lot.end_time > now)
            .order_by(Lot.end_time.asc())
        )
        result = await session.execute(query)
        return list(result.scalars().all())

    async def place_bid(
            self,
            session: AsyncSession,
            lot_id: int,
            payload: BidCreate,
    ) -> tuple[Bid, Lot, dict, dict | None]:
        lot = await session.get(Lot, lot_id, with_for_update=True)
        if lot is None:
            raise LotNotFoundError()

        lot = cast(Lot, lot)
        now = datetime.now(timezone.utc)

        if lot.status == LotStatus.ENDED or lot.end_time <= now:
            lot.status = LotStatus.ENDED
            await session.commit()
            raise LotEndedError()

        if payload.amount <= lot.current_price:
            raise BidTooLowError(str(lot.current_price))

        bid = Bid(
            lot_id=lot.id,
            bidder_id=payload.bidder.lower().replace(" ", "-"),
            bidder_name=payload.bidder,
            amount=payload.amount,
        )
        lot.current_price = payload.amount

        time_extended_event: dict | None = None
        if lot.end_time - now <= TIME_EXTENSION_WINDOW:
            lot.end_time += TIME_EXTENSION_AMOUNT
            time_extended = TimeExtended(
                type="time_extended",
                lot_id=lot.id,
                end_time=lot.end_time
            )
            time_extended_event = time_extended.model_dump(mode="json")

        session.add(bid)
        await session.commit()
        await session.refresh(bid)

        bid_placed = BidPlaced(
            type="bid_placed",
            lot_id=lot.id,
            bidder=bid.bidder_name,
            amount=bid.amount,
        )

        return (
            bid,
            lot,
            bid_placed.model_dump(mode="json"),
            time_extended_event,
        )


auction_crud = AuctionCrud()
