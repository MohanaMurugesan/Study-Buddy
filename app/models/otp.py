from app.database import Base
from sqlalchemy import Column,String,TIMESTAMP,Boolean,func
import uuid
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime,timedelta,timezone



class Otp(Base):
    __tablename__ = "otps"

    id = Column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4)
    email = Column(String,nullable=False)
    otp_code = Column(String,nullable=False)
    expires_at = Column(TIMESTAMP,nullable= False, default=lambda: datetime.now(timezone.utc) + timedelta(minutes=5))
    is_verified = Column(Boolean,default=False)
    created_at = Column(TIMESTAMP(timezone=True),server_default=func.now())
    token = Column(String,unique = True,nullable = False)
    last_requested_time = Column(TIMESTAMP(timezone=True),nullable=False)

