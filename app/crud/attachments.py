from sqlalchemy.orm import Session
from uuid import UUID
from app.models.attachments import Attachment
from app.models.community import CommunityMembership

def create_attachment(db: Session, *, message_id: UUID, file_path: str, file_name: str, file_type: str, file_size: int, user_id: UUID, community_id: UUID) -> Attachment:
    attachment = Attachment(
        message_id=message_id,
        file_path=file_path,
        file_name=file_name,
        file_type=file_type,   
        file_size=file_size,
        user_id=user_id,
        community_id=community_id,
    )
    db.add(attachment)
    db.flush()
    return attachment

def list_attachments_by_community(db: Session, *, community_id: UUID, limit: int = 50):
    return (
        db.query(Attachment)
        .filter(Attachment.community_id == community_id)
        .order_by(Attachment.created_at.desc())
        .limit(limit)
        .all()
    )

def user_is_member_of_community(db: Session, *, user_id: UUID, community_id: UUID) -> bool:
    return db.query(CommunityMembership).filter(
        CommunityMembership.community_id == community_id,
        CommunityMembership.member_id == user_id,
    ).first() is not None

def get_attachment_by_id(db: Session, *, attachment_id: UUID) -> Attachment | None:
    return db.query(Attachment).get(attachment_id)