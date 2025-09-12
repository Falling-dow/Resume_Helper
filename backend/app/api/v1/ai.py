from fastapi import APIRouter

from app.schemas.resume import OptimizeRequest, OptimizeResponse

router = APIRouter(prefix="/ai", tags=["ai"])


@router.post("/optimize", response_model=OptimizeResponse)
async def optimize(req: OptimizeRequest):
    # TODO: integrate LangChain / OpenAI
    return OptimizeResponse(
        optimized_content={"summary": "优化后的简历摘要", "sections": []},
        match_score=0.82,
        suggestions={"keywords": ["Python", "FastAPI"]},
        keywords_to_add=["异步编程", "微服务"],
    )

