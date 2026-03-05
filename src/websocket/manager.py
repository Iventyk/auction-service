from collections import defaultdict
from typing import DefaultDict

from fastapi import WebSocket


class ConnectionManager:
    def __init__(self) -> None:
        self._connections: DefaultDict[int, set[WebSocket]] = defaultdict(set)

    async def connect(self, lot_id: int, websocket: WebSocket) -> None:
        await websocket.accept()
        self._connections[lot_id].add(websocket)

    def disconnect(self, lot_id: int, websocket: WebSocket) -> None:
        self._connections[lot_id].discard(websocket)
        if not self._connections[lot_id]:
            self._connections.pop(lot_id, None)

    async def broadcast(self, lot_id: int, message: dict) -> None:
        sockets = list(self._connections.get(lot_id, set()))
        for socket in sockets:
            await socket.send_json(message)


ws_manager = ConnectionManager()
