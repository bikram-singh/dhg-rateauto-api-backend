from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional

from app.database import get_db
from app.models.pricing import Pricing
from app.models.vaccine import Vaccine
from app.models.hospital import Hospital
from app.models.department import Department
from app.schemas import PricingCreate, PricingUpdate, PricingResponse
from app.schemas import VaccineResponse, HospitalResponse, DepartmentResponse

router = APIRouter(prefix="/pricing", tags=["Pricing"])


async def enrich_pricing(p, db):
    """Manually fetch related objects."""
    vaccine = (await db.execute(select(Vaccine).where(Vaccine.id == p.vaccine_id))).scalar_one_or_none()
    hospital = (await db.execute(select(Hospital).where(Hospital.id == p.hospital_id))).scalar_one_or_none()
    department = (await db.execute(select(Department).where(Department.id == p.department_id))).scalar_one_or_none()
    return {
        "id": p.id,
        "vaccine_id": p.vaccine_id,
        "hospital_id": p.hospital_id,
        "department_id": p.department_id,
        "price": p.price,
        "insurance_covered": p.insurance_covered,
        "status": p.status,
        "created_at": p.created_at,
        "vaccine": VaccineResponse.model_validate(vaccine) if vaccine else None,
        "hospital": HospitalResponse.model_validate(hospital) if hospital else None,
        "department": DepartmentResponse.model_validate(department) if department else None,
    }


@router.get("/", response_model=List[PricingResponse])
async def list_pricing(
    skip: int = 0,
    limit: int = 100,
    vaccine_id: Optional[int] = Query(None),
    hospital_id: Optional[int] = Query(None),
    department_id: Optional[int] = Query(None),
    status: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db)
):
    query = select(Pricing).offset(skip).limit(limit)
    if vaccine_id:
        query = query.where(Pricing.vaccine_id == vaccine_id)
    if hospital_id:
        query = query.where(Pricing.hospital_id == hospital_id)
    if department_id:
        query = query.where(Pricing.department_id == department_id)
    if status:
        query = query.where(Pricing.status == status)
    result = await db.execute(query)
    items = result.scalars().all()
    return [await enrich_pricing(p, db) for p in items]


@router.get("/{pricing_id}", response_model=PricingResponse)
async def get_pricing(pricing_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Pricing).where(Pricing.id == pricing_id))
    pricing = result.scalar_one_or_none()
    if not pricing:
        raise HTTPException(status_code=404, detail="Pricing record not found")
    return await enrich_pricing(pricing, db)


@router.post("/", response_model=PricingResponse, status_code=status.HTTP_201_CREATED)
async def create_pricing(payload: PricingCreate, db: AsyncSession = Depends(get_db)):
    pricing = Pricing(**payload.model_dump())
    db.add(pricing)
    await db.commit()
    await db.refresh(pricing)
    return await enrich_pricing(pricing, db)


@router.put("/{pricing_id}", response_model=PricingResponse)
async def update_pricing(
    pricing_id: int,
    payload: PricingUpdate,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Pricing).where(Pricing.id == pricing_id))
    pricing = result.scalar_one_or_none()
    if not pricing:
        raise HTTPException(status_code=404, detail="Pricing record not found")
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(pricing, key, value)
    await db.commit()
    await db.refresh(pricing)
    return await enrich_pricing(pricing, db)


@router.delete("/{pricing_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_pricing(pricing_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Pricing).where(Pricing.id == pricing_id))
    pricing = result.scalar_one_or_none()
    if not pricing:
        raise HTTPException(status_code=404, detail="Pricing record not found")
    await db.delete(pricing)
    await db.commit()
