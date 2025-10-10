from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
from fastapi.responses import FileResponse
from uuid import UUID, uuid4
import os
import filetype
from app.models.message import Message
from app.crud.attachments import create_attachment,list_attachments_by_community,user_is_member_of_community,get_attachment_by_id
from .profile import user_dependency
from .auth import db_dependency


router = APIRouter(
    prefix="/documents",
    tags=["documents"]
)

ALLOWED_MIME = {
    "application/pdf",
    "image/png",
    "image/jpeg",
    "video/mp4",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
}

def detect_mime_from_bytes(head:bytes):
    kind = filetype.guess(head)
    return kind.mime if kind else None

@router.post("/upload",response_model=dict)
async def upload_document(file:UploadFile,community_id:UUID,db:db_dependency,user : user_dependency):
    user_id = user.id

    if not user_is_member_of_community(db,user_id = user_id , community_id=community_id):
        raise HTTPException(status_code=403,detail = "You are not a member of the community")

    
    data = await file.read()
    size_bytes = len(data)

    if size_bytes > 26214400:
        raise HTTPException(status_code=400,detail="File size is larger")


    head = data[:8192]
    detected_mime = detect_mime_from_bytes(head)
    claimed_mime = file.content_type or ""

    if not detected_mime:
        raise HTTPException(status_code=400,detail="Could not detect file type")

    if detected_mime != claimed_mime:
        raise HTTPException(status_code=400, detail=f"Type mismatch: {claimed_mime} vs {detected_mime}")

    if detected_mime not in ALLOWED_MIME:
        raise HTTPException(status_code=415, detail=f"Unsupported file type: {detected_mime}")

    save_name = os.path.basename(file.filename)
    file_uuid = uuid4()
    base_dir = os.path.join("media", str(community_id))
    os.makedirs(base_dir, exist_ok=True)
    storage_path = os.path.join(base_dir, f"{file_uuid}_{save_name}")
    with open(storage_path, "wb") as f:
        f.write(data)

    text = f"{user.username} sent a {'image' if detected_mime.startswith('image/') else 'document'}"
    message = Message(
        sender_id=user_id,
        community_id=community_id,
        message=text,
    )
    db.add(message)
    db.flush()  


    attachment = create_attachment(
        db,
        message_id=message.id,
        file_path=storage_path,
        file_name=save_name,
        file_type=detected_mime,   
        file_size=size_bytes,
        user_id=user_id,
        community_id=community_id,
    )

    db.commit()

    document_url = f"/documents/attchements/{attachment.id}"  
    download_url = f"/attachments/{attachment.id}"                    

    return {
        "message": {"id": str(message.id), "text": text},
        "attachment": {
            "id": str(attachment.id),
            "file_name": attachment.file_name,
            "file_type": attachment.file_type,
            "file_size": attachment.file_size,
            "created_at": attachment.created_at.isoformat(),
            "downloadUrl": download_url,
            "documentUrl": document_url,
        },
    }

@router.get("/list/{community_id}", response_model=list[dict])
def list_documents(community_id: UUID, db: db_dependency, user: user_dependency):

    if not user_is_member_of_community(db, user_id=user.id, community_id=community_id):
        raise HTTPException(status_code=403, detail="Not a community member")

    items = list_attachments_by_community(db, community_id=community_id, limit=200)
    return [
        {
            "id": str(a.id),
            "file_name": a.file_name,
            "file_type": a.file_type,
            "file_size": a.file_size,
            "created_at": a.created_at.isoformat(),
            "uploaded_by": str(a.user_id),
            "downloadUrl": f"/attachments/{a.id}",
            "documentUrl": f"/chats/{a.community_id}/documents/{a.id}",
        }
        for a in items
    ]

@router.get("/attachments/{attachment_id}")
def download_attachment(attachment_id: UUID, db: db_dependency, current_user:user_dependency):
    attachment = get_attachment_by_id(db, attachment_id=attachment_id)
    if not attachment:
        raise HTTPException(status_code=404, detail="Attachment not found")

    if not user_is_member_of_community(db, user_id=current_user.id, community_id=attachment.community_id):
        raise HTTPException(status_code=403, detail="Not allowed")

    if not os.path.exists(attachment.file_path):
        raise HTTPException(status_code=410, detail="File no longer available")

    return FileResponse(
        path=attachment.file_path,
        media_type=attachment.file_type,
        filename=attachment.file_name,
    )