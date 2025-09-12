from uuid import UUID

from fastapi import APIRouter

router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.get("")
def list_jobs(page: int = 1, size: int = 10):
    # TODO: query DB and support filters
    items = [
        {
            "id": "00000000-0000-0000-0000-000000000001",
            "title": "后端开发工程师",
            "company": "某互联网公司",
            "location": "上海",
            "salary_min": 20000,
            "salary_max": 35000,
            "experience_level": "3-5年",
            "industry": "互联网",
            "description": "负责后端服务开发",
        }
    ]
    return {"items": items, "page": page, "size": size, "total": 1}


@router.get("/{job_id}")
def get_job(job_id: UUID):
    # TODO: fetch from DB
    return {
        "id": str(job_id),
        "title": "后端开发工程师",
        "company": "某互联网公司",
        "location": "上海",
        "description": "岗位详情...",
    }

