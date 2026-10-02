from fastapi import APIRouter
from app.api.v1.endpoints import funds, health, items, locations, query, schemes

api_router = APIRouter()

# Include endpoint routers
api_router.include_router(health.router, tags=["Health"])
api_router.include_router(query.router, prefix="/query", tags=["AI Natural Language Query"])
api_router.include_router(schemes.router, prefix="/schemes", tags=["Government Schemes"])
api_router.include_router(locations.router, prefix="/locations", tags=["Locations"])
api_router.include_router(funds.router, prefix="/funds", tags=["Fund Allocations"])
api_router.include_router(items.router, prefix="/items", tags=["Items"])
