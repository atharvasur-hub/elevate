from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.location import Location
from app.schemas.location import LocationCreate, LocationResponse, LocationUpdate

router = APIRouter()


@router.get("/", response_model=List[LocationResponse], summary="List all locations")
async def get_locations(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    state: Optional[str] = None,
    district: Optional[str] = None,
    sub_district: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    query = select(Location)
    if state:
        query = query.where(Location.state.ilike(f"%{state}%"))
    if district:
        query = query.where(Location.district.ilike(f"%{district}%"))
    if sub_district:
        query = query.where(Location.sub_district.ilike(f"%{sub_district}%"))

    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()


@router.post("/", response_model=LocationResponse, status_code=status.HTTP_201_CREATED, summary="Create a new location")
async def create_location(
    location_in: LocationCreate,
    db: AsyncSession = Depends(get_db),
):
    location = Location(**location_in.model_dump())
    db.add(location)
    await db.commit()
    await db.refresh(location)
    return location


@router.get("/{location_id}", response_model=LocationResponse, summary="Get location by ID")
async def get_location(
    location_id: int,
    db: AsyncSession = Depends(get_db),
):
    location = await db.get(Location, location_id)
    if not location:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Location not found")
    return location


@router.put("/{location_id}", response_model=LocationResponse, summary="Update location")
async def update_location(
    location_id: int,
    location_in: LocationUpdate,
    db: AsyncSession = Depends(get_db),
):
    location = await db.get(Location, location_id)
    if not location:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Location not found")

    update_data = location_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(location, field, value)

    await db.commit()
    await db.refresh(location)
    return location


@router.delete("/{location_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete location")
async def delete_location(
    location_id: int,
    db: AsyncSession = Depends(get_db),
):
    location = await db.get(Location, location_id)
    if not location:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Location not found")

    await db.delete(location)
    await db.commit()
    return None
