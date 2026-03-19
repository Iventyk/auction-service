"""Service layer for auction workflows."""

from sqlalchemy.ext.asyncio import AsyncSession

from src.crud import auction_crud
from src.schemas.auction import BidCreate, LotCreate


async def create_lot(session: AsyncSession, payload: LotCreate):
    return await auction_crud.create_lot(session=session, payload=payload)


async def get_active_lots(session: AsyncSession):
    return await auction_crud.get_active_lots(session=session)


async def place_bid(session: AsyncSession, lot_id: int, payload: BidCreate):
    return await auction_crud.place_bid(
        session=session,
        lot_id=lot_id,
        payload=payload,
    )
