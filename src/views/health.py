from fastapi import APIRouter

from src.components.base_response.schema import BaseResponse


router = APIRouter()


@router.get("/", response_model=BaseResponse, status_code=200)
async def health_check_endpoint():
    try:
        return BaseResponse(
            message="It's OK!",
            success=True
        )
    except Exception as error: 
        return BaseResponse(
            message=f"Pipec: {str(error)}",
            success=False
        )
