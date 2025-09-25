from sqlalchemy.orm import Session,joinedload
from app.models.message import Message
from app.schemas.message import MessageCreate
import uuid


def create_message(db: Session, sender_id: uuid.UUID, message_data: MessageCreate):
    message = Message(
        sender_id=sender_id,
        community_id=message_data.community_id,
        message=message_data.message,
    )
    db.add(message)
    db.commit()
    db.refresh(message)
    return message


def get_messages_by_community(db: Session, community_id: uuid.UUID, limit: int = 500):
    messages = (
        db.query(Message)
        .filter(Message.community_id == community_id)
        .options(joinedload(Message.sender)) 
        .order_by(Message.created_at.desc())
        .limit(limit)
        .all()
    )
    return list(reversed(messages)) 


def get_message(db: Session, message_id: uuid.UUID):
    message = db.query(Message).filter(Message.id == message_id).first()
    if not message:
        return None
        #raise HTTPException(status_code=404, detail="Message not found")
    return message


def delete_message(db: Session, message_id: uuid.UUID, sender_id: uuid.UUID):
    message = db.query(Message).filter(Message.id == message_id).first()
    if not message:
        return 1
        #raise HTTPException(status_code=404, detail="Message not found")

    if message.sender_id != sender_id:
        return 2
        #raise HTTPException(status_code=403, detail="Not authorized to delete this message")

    db.delete(message)
    db.commit()
    return {"detail": "Message deleted successfully"}


