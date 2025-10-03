from fastapi import APIRouter, HTTPException, status
from models.exoplanet import ExoplanetData, Response
from services.exoplanet_service import ExoplanetService
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/exoplanet")

exoplanet_service = ExoplanetService()

@router.post(
    "/",
    response_model=Response,
    status_code=status.HTTP_200_OK,
)
async def process_exoplanet_data(data: ExoplanetData):
    try:
        response = await exoplanet_service.process_exoplanet_data(data)
        return response
        
    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Validation error: {str(e)}"
        )
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while processing the data"
        )
