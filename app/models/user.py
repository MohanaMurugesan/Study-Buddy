from app.database import Base
from sqlalchemy import Column,String,TIMESTAMP,Boolean,func,JSON
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy.orm import relationship



class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4)
    email = Column(String,unique=True,nullable=False)
    username = Column(String,unique=True,nullable=False)
    password = Column(String,nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),server_default=func.now())
    is_verified = Column(Boolean,default=False)


    profile = relationship("Profile", back_populates="user", uselist=False)
    communities=relationship("Community",back_populates="owner")
    community_membership = relationship("CommunityMembership",back_populates="member")


    



