from fastapi import (
    HTTPException,
    Depends,
    WebSocket,
    APIRouter,
)
from fastapi.responses import HTMLResponse
from starlette.websockets import WebSocketDisconnect
from backend.routers.auth import get_current_user
from backend.schemas.schemas import users
from veiws.veiw import html

router = APIRouter(
    prefix="/chat", tags=["chat"], responses={404: {"description": "Not found"}}
)


class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[int:WebSocket] = {}

    async def connect(self, websocket: WebSocket, id1: int):
        await websocket.accept()
        self.active_connections[id1] = websocket

    def disconnect(self, websocket: WebSocket, id1: int):
        self.active_connections.pop(id1)

    async def send_personal_message(
        self, id1: int, message: str, websocket: WebSocket
    ):
        await websocket.send_text(message)
        if id1 in self.active_connections:
            await self.active_connections[id1].send_text(message)


manager = ConnectionManager()


@router.get("/{user_id}/{receiver}")
async def get(
    user_id: int,
    receiver: int,
    current_user_id: int = Depends(get_current_user),
):
    if (
        user_id != current_user_id
        or receiver not in users.get_user(user_id).friends
    ):
        raise HTTPException(status_code=404, detail="No access to chat")
        # raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)

    return HTMLResponse(html.format(str(user_id), str(receiver)))


@router.websocket("/ws/{user_id}/{receiver}")
async def websocket_endpoint(websocket: WebSocket, user_id: int, receiver: int):
    await manager.connect(websocket, user_id)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(
                receiver, f"User {user_id} wrote: {data}", websocket
            )
    except WebSocketDisconnect:
        manager.disconnect(websocket, user_id)
        await manager.send_personal_message(
            receiver, f"Client #{user_id} left the chat", websocket
        )
