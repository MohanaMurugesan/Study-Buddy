from fastapi import APIRouter,status,HTTPException
from app.routers.auth import db_dependency
from app.schemas.community import CommunityCreate,CommunityResponse,CommunityUpdate,MembershipCreate,CommunitiesOfMember
from app.crud import community as community_crud
from .profile import user_dependency
import uuid
from app.enums import CommunityRole
from typing import List

router = APIRouter(
    prefix="/communities",
    tags=["communities"]
)

@router.post("/create-community",response_model=CommunityResponse,status_code=status.HTTP_201_CREATED)
def create_community(community_create:CommunityCreate,
                     db:db_dependency,
                     user:user_dependency):
    
    community_record=community_crud.get_community_by_name(db,community_create.community_name)
    if community_record:
        raise HTTPException(status_code=400,detail="Community name already exist")
    
    newcommunity = community_crud.new_community(db,user.id,community_create)
    
    return newcommunity


@router.get("/all-communities",status_code=status.HTTP_200_OK)
def get_all_communities(db:db_dependency,user:user_dependency):
    all_community = community_crud.get_all_community(db)
    if not all_community:
        return {"detail":"No community found"}
    return all_community

@router.get("/get-community-by-id/{community_id}",status_code=status.HTTP_200_OK)
def get_communities_by_id(db:db_dependency,user:user_dependency,community_id:uuid.UUID):
    community_by_id = community_crud.get_community_by_id(db,community_id)
    if not community_by_id:
        raise HTTPException(status_code=404,detail="No community found")
    return community_by_id

@router.get("/get-community-by-name/{community_name}",status_code=status.HTTP_200_OK)
def get_community_by_name(db:db_dependency,user:user_dependency,community_name:str):
    community_by_name = community_crud.get_community_by_name(db,community_name)
    if not community_by_name:
        raise HTTPException(status_code=404,detail="No community found")
    return community_by_name

@router.get("/get-all-members-in-community/{community_id}",status_code=status.HTTP_200_OK)
def get_all_members_in_community(db:db_dependency,user:user_dependency,community_id:uuid.UUID):
    all_members = community_crud.get_all_members(db,community_id)
    if not all_members:
        raise HTTPException(status_code=404,detail="No members found")
    return all_members

@router.patch("/update-community/{id}",status_code=status.HTTP_200_OK)
def updating_community(db:db_dependency,user:user_dependency,community_id:uuid.UUID,updatecommunity:CommunityUpdate):
    result= community_crud.update_community(db,community_id,user.id,updatecommunity)
    if not result:
        raise HTTPException(status_code=401,detail="You don't have permission to update the community")
    return {"detail": "Updated successfully"}

@router.delete("/delete-community/{id}",status_code=status.HTTP_200_OK)
def deleting_community(db:db_dependency,user:user_dependency,community_id:uuid.UUID):
    result = community_crud.delete_community(db,community_id,user.id)
    if not result:
        raise HTTPException(status_code=401,detail="Unauthroized,You don't have permission to delete")
    return {"detail":"Community deleted successfully"}

@router.post("/join-community/{id}/join",status_code=status.HTTP_200_OK)
def join_community(db:db_dependency,user:user_dependency,membership:MembershipCreate):
    adding_member = community_crud.add_member(db,user.id,membership)
    if not adding_member:
        raise HTTPException(status_code=404,detail="Failed to add member")
    return {"detail":"Member added successfully"}

@router.delete("/leave-community/{id}/leave",status_code=status.HTTP_200_OK)
def leave_community(db:db_dependency,
                    user:user_dependency,
                    community_id:uuid.UUID):
    result= community_crud.leave_community(db,community_id,user.id)

    if result == 2:
        raise HTTPException(status_code=404,detail="You are not a member")
    
    elif result == 3:
        raise HTTPException(status_code=404,detail="You are the owner")

    return {"detail":"Successfully left the community"}


@router.delete("/remove-member/{member_id}/remove",status_code=status.HTTP_200_OK)
def remove_member(db:db_dependency,
                  user:user_dependency,
                  community_id:uuid.UUID,
                  member_id:uuid.UUID):
    result= community_crud.remove_member(db,member_id,community_id,user.id)
    if  result == 3:
        raise HTTPException(status_code=404,detail="User not found")
    
    elif result == 2:
        raise HTTPException(status_code=403,detail="You don't have permission to remove user")
    
    elif result == 4:
        raise HTTPException(status_code=403,detail="Community owner cannot be removed")

    return {"detail":"Removed member successfully"}

@router.patch("/update-role/{community_id}/{target_id}/{role}",status_code=status.HTTP_200_OK)
def update_role(db:db_dependency,
                user:user_dependency,
                target_id:uuid.UUID,
                community_id:uuid.UUID,
                role:CommunityRole ):
    result= community_crud.change_role(db,target_id,community_id,user.id,role)

    if result == 2:
        raise HTTPException(status_code=401,detail="You're not the member of the community")
    
    elif result == 3:
        raise HTTPException(status_code=404,detail="User not found")
    
    elif result == 4:
        raise HTTPException(status_code=403,detail="You don't have permission to change the role")
    
    elif result ==5:
        raise HTTPException(status_code=403,detail="Only owner can chang the role to owner")
    
    elif result ==6:
        raise HTTPException(status_code=403,detail="You can't change the owner's role")
    
    return {"detail":"Role changed successfully"}

@router.get("/all-communities-of-a-member",response_model=List[CommunitiesOfMember],status_code=status.HTTP_200_OK)
def get_communities_of_a_member(db:db_dependency,user:user_dependency):
    communities = community_crud.get_communities_of_a_member(db,user.id)
    if not communities:
        return {"detail":"No communities found"}
    return communities