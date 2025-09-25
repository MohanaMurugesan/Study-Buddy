from typing import Dict, List
from fastapi import WebSocket

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}  # community_id -> list of connections

    async def connect(self, community_id: str, websocket: WebSocket):
        if community_id not in self.active_connections:
            self.active_connections[community_id] = []
        self.active_connections[community_id].append(websocket)

    def disconnect(self, community_id: str, websocket: WebSocket):
        self.active_connections[community_id].remove(websocket)
        if not self.active_connections[community_id]:
            del self.active_connections[community_id]

    async def broadcast(self, community_id: str, message: dict):
        if community_id in self.active_connections:
            for connection in self.active_connections[community_id]:
                await connection.send_json(message)
