from fastapi import APIRouter
from app.core.config import settings
from app.core.database import check_database_connection
from app.schemas.health import DatabaseStatus, HealthCheckResponse

router = APIRouter()


@router.get("/health", response_model=HealthCheckResponse, summary="Service & Supabase Health Status")
async def health_check():
    """
    Performs a live health check on the FastAPI application and verifies
    the PostgreSQL connection to Supabase.
    """
    db_status = await check_database_connection()

    overall_status = "healthy" if db_status.get("status") == "healthy" else "degraded"

    return HealthCheckResponse(
        app_name=settings.PROJECT_NAME,
        version=settings.PROJECT_VERSION,
        environment=settings.ENVIRONMENT,
        status=overall_status,
        database=DatabaseStatus(**db_status),
    )
