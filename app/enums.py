from enum import Enum

class CommunityRole(Enum):
    OWNER = "OWNER"
    ADMIN = "ADMIN"
    MEMBER = "MEMBER"

class Status(Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"