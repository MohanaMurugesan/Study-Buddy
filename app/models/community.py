from app.database import Base
from sqlalchemy import Column,UUID,String,Text,ForeignKey,DateTime,Boolean,Enum
import uuid
from datetime import datetime,timezone
from sqlalchemy.orm import relationship
from app.enums import CommunityRole,Status


class Community(Base):
    __tablename__ = "community"

    id = Column(UUID(as_uuid=True),nullable = False,primary_key=True,default=uuid.uuid4)
    community_name = Column(String,nullable = False,index=True)
    subject = Column(String,nullable=False)
    goals = Column(String,nullable=True)
    description = Column(Text,nullable=True)
    owner_id = Column(UUID(as_uuid=True),ForeignKey("users.id",ondelete="CASCADE"),nullable=False)
    created_at = Column(DateTime,default=lambda:datetime.now(timezone.utc))
    updated_at = Column(DateTime,default=lambda:datetime.now(timezone.utc),onupdate=lambda:datetime.now(timezone.utc))
    is_private=Column(Boolean,default=False)


    owner=relationship("User",back_populates="communities")
    membership=relationship("CommunityMembership",back_populates="community",cascade="all,delete-orphan")

class CommunityMembership(Base):
    __tablename__="community_members"

    community_id = Column(UUID(as_uuid=True),ForeignKey("community.id",ondelete="CASCADE"),primary_key=True)
    member_id = Column(UUID(as_uuid=True),ForeignKey("users.id",ondelete="CASCADE"),primary_key=True)
    role = Column(Enum(CommunityRole,name="community_role"),nullable=False,default=CommunityRole.MEMBER.value)
    joined_at = Column(DateTime,default=lambda:datetime.now(timezone.utc))
    status = Column(Enum(Status,name="status"),nullable=False,default=Status.ACTIVE.value)

    community=relationship("Community",back_populates="membership")
    member = relationship("User",back_populates="community_membership")