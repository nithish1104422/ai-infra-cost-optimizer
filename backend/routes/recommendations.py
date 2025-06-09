from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend.ai_agent.summarizer import generate_summary

router = APIRouter()

class ResourceInput(BaseModel):
    resource_name: str
    resource_type: str
    usage_data: str
    recommendation: str

@router.post("/recommendation")
async def get_ai_recommendation(input_data: ResourceInput):
    try:
        summary = generate_summary(
            input_data.resource_name,
            input_data.resource_type,
            input_data.usage_data,
            input_data.recommendation
        )
        return {"summary": summary}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
