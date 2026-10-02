from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.scheme import Scheme
from app.schemas.scheme import SchemeCreate, SchemeResponse, SchemeUpdate

router = APIRouter()


@router.get("/", response_model=List[SchemeResponse], summary="List all government schemes")
async def get_schemes(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    sector: Optional[str] = None,
    ministry: Optional[str] = None,
    is_active: Optional[bool] = None,
    db: AsyncSession = Depends(get_db),
):
    query = select(Scheme)
    if sector:
        query = query.where(Scheme.sector.ilike(f"%{sector}%"))
    if ministry:
        query = query.where(Scheme.ministry.ilike(f"%{ministry}%"))
    if is_active is not None:
        query = query.where(Scheme.is_active == is_active)

    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()


@router.post("/", response_model=SchemeResponse, status_code=status.HTTP_201_CREATED, summary="Create a new scheme")
async def create_scheme(
    scheme_in: SchemeCreate,
    db: AsyncSession = Depends(get_db),
):
    # Check if code already exists
    existing = await db.execute(select(Scheme).where(Scheme.code == scheme_in.code))
    if existing.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Scheme with code '{scheme_in.code}' already exists",
        )

    scheme = Scheme(**scheme_in.model_dump())
    db.add(scheme)
    await db.commit()
    await db.refresh(scheme)
    return scheme


@router.get("/{scheme_id}", response_model=SchemeResponse, summary="Get scheme by ID")
async def get_scheme(
    scheme_id: int,
    db: AsyncSession = Depends(get_db),
):
    scheme = await db.get(Scheme, scheme_id)
    if not scheme:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Scheme not found")
    return scheme


@router.put("/{scheme_id}", response_model=SchemeResponse, summary="Update scheme")
async def update_scheme(
    scheme_id: int,
    scheme_in: SchemeUpdate,
    db: AsyncSession = Depends(get_db),
):
    scheme = await db.get(Scheme, scheme_id)
    if not scheme:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Scheme not found")

    update_data = scheme_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(scheme, field, value)

    await db.commit()
    await db.refresh(scheme)
    return scheme


@router.delete("/{scheme_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete scheme")
async def delete_scheme(
    scheme_id: int,
    db: AsyncSession = Depends(get_db),
):
    scheme = await db.get(Scheme, scheme_id)
    if not scheme:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Scheme not found")

    await db.delete(scheme)
    await db.commit()
    return None
