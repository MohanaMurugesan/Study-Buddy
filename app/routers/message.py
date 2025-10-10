from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.crud import message as message_crud
from app.schemas.message import MessageCreate, MessageResponse
from app.utils.connection_manager import ConnectionManager
from app.database import SessionLocal
from app.utils.jwt import decode_access_token  
import uuid
from app.routers.auth import db_dependency
from app.routers.profile import user_dependency
from typing import List
import json
from app.crud import community as community_crud


router = APIRouter(
    prefix="/messages",
    tags=["chat"]
)

manager = ConnectionManager()


@router.websocket("/community/{community_id}")
async def community_chat(websocket: WebSocket, community_id: str):
    # 1. Accept the connection
    await websocket.accept()

    # 2. Extract JWT token from query params
    token = websocket.query_params.get("token")
    if not token:
        await websocket.close(code=4001)
        return

    # 3. Decode JWT token
    try:
        payload = decode_access_token(token)  # your existing JWT decode function
        user_id = payload.get("sub")   # "sub" usually stores user.id
        if not user_id:
            await websocket.close(code=4002)
            return
    except Exception:
        await websocket.close(code=4002)
        return

    # 4. Open a manual DB session
    db = SessionLocal()

    is_member = community_crud.is_user_in_community(db, user_id=uuid.UUID(user_id), community_id=uuid.UUID(community_id))
    if not is_member:
        await websocket.close(code=4003)  # Custom code for "not a member"
        db.close()
        return

    # 5. Register the user’s connection in the ConnectionManager
    await manager.connect(community_id, websocket)

    try:
        while True:
            # 6. Receive message from this client (support JSON or plain text)
            raw_text = await websocket.receive_text()
            try:
                parsed = json.loads(raw_text)
                text = parsed.get("message", raw_text)
            except Exception:
                text = raw_text

            if not text:
                continue

            # 7. Save message in DB
            message_create = MessageCreate(
                message=text,
                community_id=uuid.UUID(community_id)
            )
            saved_message = message_crud.create_message(
                db, sender_id=uuid.UUID(user_id), message_data=message_create
            )

            # 8. Convert to response schema (serialize UUIDs and datetimes)
            message_dict = MessageResponse.from_orm(saved_message).model_dump(mode="json")
            # 9. Broadcast message to everyone in this community
            await manager.broadcast(community_id, message_dict)

    except WebSocketDisconnect:
        manager.disconnect(community_id, websocket)
    finally:
        db.close()

@router.get("/community/{community_id}/history",response_model=List[MessageResponse])
def get_chat_history(
    db : db_dependency,
    user : user_dependency,
    community_id :uuid.UUID,
    limit : int = 75,
):
    return message_crud.get_messages_by_community(db,community_id,limit)