from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from src.websocket.manager import ws_manager

ws_router = APIRouter(tags=["ws"])


@ws_router.websocket("/ws/lots/{lot_id}")
async def lot_events_socket(lot_id: int, websocket: WebSocket) -> None:
    await ws_manager.connect(lot_id=lot_id, websocket=websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        ws_manager.disconnect(lot_id=lot_id, websocket=websocket)
