from uuid import UUID, uuid4

from fastapi import APIRouter, UploadFile

router = APIRouter(prefix="/resumes", tags=["resumes"])


@router.get("")
def list_resumes():
    return {"items": []}


@router.get("/{resume_id}")
def get_resume(resume_id: UUID):
    return {"id": str(resume_id), "title": "我的简历", "version": 1}


@router.post("/upload")
async def upload_resume(file: UploadFile):
    # TODO: save to object storage and create DB record
    rid = uuid4()
    return {"id": str(rid), "file_url": f"/uploads/{rid}-{file.filename}", "file_type": file.content_type}

