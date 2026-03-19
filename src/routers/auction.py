from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.config.dependencies import get_db_session
from src.services import auction as auction_service
from src.schemas.auction import BidCreate, BidRead, LotCreate, LotRead
from src.websocket.manager import ws_manager

router = APIRouter(tags=["lots"])


@router.post("/lots", response_model=LotRead, status_code=201)
async def create_lot_endpoint(
    payload: LotCreate,
    session: AsyncSession = Depends(get_db_session),
) -> LotRead:
    lot = await auction_service.create_lot(session=session, payload=payload)
    return LotRead.model_validate(lot)


@router.get("/lots", response_model=list[LotRead])
async def get_active_lots_endpoint(
    session: AsyncSession = Depends(get_db_session),
) -> list[LotRead]:
    lots = await auction_service.get_active_lots(session=session)
    return [LotRead.model_validate(lot) for lot in lots]


@router.post("/lots/{lot_id}/bids", response_model=BidRead, status_code=201)
async def place_bid_endpoint(
    lot_id: int,
    payload: BidCreate,
    session: AsyncSession = Depends(get_db_session),
) -> BidRead:
    bid, lot, bid_event, extension_event = await auction_service.place_bid(
        session=session,
        lot_id=lot_id,
        payload=payload,
    )

    await ws_manager.broadcast(lot.id, bid_event)

    if extension_event:
        await ws_manager.broadcast(lot.id, extension_event)

    return BidRead.model_validate(bid)
