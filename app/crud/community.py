from sqlalchemy.orm import Session,joinedload
from app.models.community import Community,CommunityMembership
from app.schemas.community import CommunityCreate,CommunityResponse,CommunityUpdate,MembershipCreate,MemberInfo
import uuid
from app.enums import CommunityRole
from sqlalchemy import func,or_



def new_community(db: Session,owner_id:uuid.UUID,community_data:CommunityCreate):
    
    new_community = Community(**community_data.model_dump(exclude_unset=True),
                              owner_id=owner_id)
    db.add(new_community)
    db.flush()

    new_member = CommunityMembership(community_id = new_community.id,
                                     member_id = owner_id,
                                     role = CommunityRole.OWNER.value
                                     )
    db.add(new_member)
    db.commit()   

    return build_community_response(new_community)

def build_community_response(community:Community) -> CommunityResponse:
    members=[]
    for m in community.membership:
        if m.member:
            members.append(MemberInfo(
                id=m.member.id,
                username = m.member.username,
                role=m.role,
                status=m.status
                )
            )
    return CommunityResponse(
        id = community.id,
        community_name=community.community_name,
        subject=community.subject,
        is_private=community.is_private,
        created_at= community.created_at,
        updated_at = community.updated_at,
        goals= community.goals,
        description=community.description,
        membership=members
    )


def get_all_community(db:Session):
    return db.query(Community).all()

def get_community_by_name(db:Session,community_name:str):
    return (db.query(Community).filter(
        or_(
            Community.community_name.ilike(f"%{community_name}%"),
            func.similarity(Community.community_name,community_name) > 0.3
        )
    )
    .order_by(func.similarity(Community.community_name,community_name).desc())
    .all()
    )

def get_community_by_id(db:Session,community_id : uuid.UUID):
    return db.query(Community).filter(Community.id == community_id).first()

def get_all_members(db:Session,community_id:uuid.UUID):
    member=(db.query(CommunityMembership)
        .options(joinedload(CommunityMembership.member))
        .filter(CommunityMembership.community_id == community_id)
        .all())
    return member
    

def update_community(db:Session,community_id:uuid.UUID,user_id:uuid.UUID,community_data:CommunityUpdate):
    membership=db.query(CommunityMembership).filter(
        CommunityMembership.community_id == community_id ,
        CommunityMembership.member_id == user_id,
        CommunityMembership.role.in_(["OWNER","ADMIN"])
    ).first()

    if not membership:
        return None
    
    updating_community = db.query(Community).filter(Community.id == community_id).first()

    if not updating_community:
        return None
    
    for field,value in community_data.model_dump(exclude_unset=True).items():
        setattr(updating_community,field,value)

    db.add(updating_community)
    db.commit()
    db.refresh(updating_community)

    return updating_community

def delete_community(db:Session,community_id : uuid.UUID,owner_id:uuid.UUID):
    community_to_delete=db.query(Community).filter(Community.id == community_id).first()
    if community_to_delete and community_to_delete.owner_id == owner_id :
        db.delete(community_to_delete)
        db.commit()
        return True
    else:
        return None
    

def add_member(db:Session,member_id:uuid.UUID,add_community_member:MembershipCreate):
    check_member=db.query(CommunityMembership).filter(
        CommunityMembership.member_id == member_id,
        CommunityMembership.community_id == add_community_member.community_id).first()
    if check_member:
        return None
    member_data = CommunityMembership(
        **add_community_member.model_dump(exclude_unset=True),
        member_id = member_id)
    db.add(member_data)
    db.commit()
    db.refresh(member_data)
    return member_data

def remove_member(db: Session, member_id: uuid.UUID, community_id: uuid.UUID, acting_user_id: uuid.UUID):
    # Get the role of the acting user
    acting_membership = db.query(CommunityMembership).filter(
        CommunityMembership.member_id == acting_user_id,
        CommunityMembership.community_id == community_id
    ).first()

    if not acting_membership or acting_membership.role.value not in [CommunityRole.OWNER.value, CommunityRole.ADMIN.value]:
        # Acting user is not allowed
        return 2  

    # Get the target member
    target_membership = db.query(CommunityMembership).filter(
        CommunityMembership.member_id == member_id,
        CommunityMembership.community_id == community_id
    ).first()

    if not target_membership:
        return 3  # Member doesn’t exist in this community
    
    if target_membership.role.value == CommunityRole.OWNER.value:
        return 4  # cannot remove owner

    # Delete the target membership
    db.delete(target_membership)
    db.commit()
    return True

    
def leave_community(db:Session,community_id:uuid.UUID,member_id:uuid.UUID):
    member = db.query(CommunityMembership).filter(
        CommunityMembership.member_id == member_id,
        CommunityMembership.community_id == community_id
        ).first()
    
    if not member:
        return 2
    
    if member.role.value ==  CommunityRole.OWNER.value:
        return 3
        
    db.delete(member)
    db.commit()
    return True
    
def change_role(db:Session,
                target_member_id:uuid.UUID,
                community_id:uuid.UUID,
                acting_user_id:uuid.UUID,
                new_role:CommunityRole):
    
    acting_member = db.query(CommunityMembership).filter(
        CommunityMembership.community_id == community_id,
        CommunityMembership.member_id == acting_user_id
    ).first()

    if not acting_member :
        return 2
    

    target_member = db.query(CommunityMembership).filter(
        CommunityMembership.community_id == community_id,
        CommunityMembership.member_id == target_member_id
    ).first()
    
    if not target_member:
        return 3
    
    if acting_member.role.value not in [CommunityRole.OWNER.value,CommunityRole.ADMIN.value]:
        return 4
    
    if new_role == CommunityRole.OWNER:
        if acting_member.role.value != CommunityRole.OWNER.value:
            return 5
        
        acting_member.role = CommunityRole.ADMIN.value
        target_member.role = CommunityRole.OWNER.value
        db.commit()
        return True
    
    if new_role in [CommunityRole.ADMIN,CommunityRole.MEMBER]:
        if target_member.role == CommunityRole.OWNER and acting_member.role != CommunityRole.OWNER:
            return 6 
           
        target_member.role = new_role
        db.commit()
        return True
        
         
def get_communities_of_a_member(db:Session,member_id:uuid.UUID):
    communities = (db.query(Community.id,Community.community_name,CommunityMembership.role)
                    .join(Community,CommunityMembership.community_id == Community.id)
                    .filter(CommunityMembership.member_id == member_id)
                    ).all()
    if not communities:
        return None
    return communities  