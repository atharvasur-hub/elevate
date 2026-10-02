from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.database import get_db
from app.models.fund import Fund
from app.models.location import Location
from app.models.scheme import Scheme
from app.schemas.fund import FundCreate, FundDetailResponse, FundResponse, FundUpdate

router = APIRouter()


@router.get("/", response_model=List[FundDetailResponse], summary="List all funds with scheme and location details")
async def get_funds(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    scheme_id: Optional[int] = None,
    location_id: Optional[int] = None,
    financial_year: Optional[str] = None,
    status_filter: Optional[str] = Query(None, alias="status"),
    db: AsyncSession = Depends(get_db),
):
    query = (
        select(Fund)
        .options(selectinload(Fund.scheme), selectinload(Fund.location))
        .offset(skip)
        .limit(limit)
    )
    if scheme_id:
        query = query.where(Fund.scheme_id == scheme_id)
    if location_id:
        query = query.where(Fund.location_id == location_id)
    if financial_year:
        query = query.where(Fund.financial_year == financial_year)
    if status_filter:
        query = query.where(Fund.status.ilike(f"%{status_filter}%"))

    result = await db.execute(query)
    return result.scalars().all()


@router.post("/", response_model=FundResponse, status_code=status.HTTP_201_CREATED, summary="Allocate/Create a new fund entry")
async def create_fund(
    fund_in: FundCreate,
    db: AsyncSession = Depends(get_db),
):
    # Verify scheme and location exist
    scheme = await db.get(Scheme, fund_in.scheme_id)
    if not scheme:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Scheme with id {fund_in.scheme_id} does not exist",
        )

    location = await db.get(Location, fund_in.location_id)
    if not location:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Location with id {fund_in.location_id} does not exist",
        )

    fund = Fund(**fund_in.model_dump())
    db.add(fund)
    await db.commit()
    await db.refresh(fund)
    return fund


@router.get("/{fund_id}", response_model=FundDetailResponse, summary="Get fund details by ID")
async def get_fund(
    fund_id: int,
    db: AsyncSession = Depends(get_db),
):
    query = (
        select(Fund)
        .options(selectinload(Fund.scheme), selectinload(Fund.location))
        .where(Fund.id == fund_id)
    )
    result = await db.execute(query)
    fund = result.scalar_one_or_none()
    if not fund:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Fund record not found")
    return fund


@router.put("/{fund_id}", response_model=FundResponse, summary="Update fund record")
async def update_fund(
    fund_id: int,
    fund_in: FundUpdate,
    db: AsyncSession = Depends(get_db),
):
    fund = await db.get(Fund, fund_id)
    if not fund:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Fund record not found")

    update_data = fund_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(fund, field, value)

    await db.commit()
    await db.refresh(fund)
    return fund


@router.delete("/{fund_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete fund record")
async def delete_fund(
    fund_id: int,
    db: AsyncSession = Depends(get_db),
):
    fund = await db.get(Fund, fund_id)
    if not fund:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Fund record not found")

    await db.delete(fund)
    await db.commit()
    return None
