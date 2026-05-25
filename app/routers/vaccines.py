from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.database import get_db
from app.models import Vaccine
from app.schemas import VaccineCreate, VaccineResponse

router = APIRouter(prefix="/vaccines", tags=["Vaccines"])


@router.get("/", response_model=List[VaccineResponse])
async def list_vaccines(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Vaccine).offset(skip).limit(limit))
    return result.scalars().all()


@router.get("/{vaccine_id}", response_model=VaccineResponse)
async def get_vaccine(vaccine_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Vaccine).where(Vaccine.id == vaccine_id))
    vaccine = result.scalar_one_or_none()
    if not vaccine:
        raise HTTPException(status_code=404, detail="Vaccine not found")
    return vaccine


@router.post("/", response_model=VaccineResponse, status_code=status.HTTP_201_CREATED)
async def create_vaccine(payload: VaccineCreate, db: AsyncSession = Depends(get_db)):
    vaccine = Vaccine(**payload.model_dump())
    db.add(vaccine)
    await db.commit()
    await db.refresh(vaccine)
    return vaccine


@router.put("/{vaccine_id}", response_model=VaccineResponse)
async def update_vaccine(
    vaccine_id: int,
    payload: VaccineCreate,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Vaccine).where(Vaccine.id == vaccine_id))
    vaccine = result.scalar_one_or_none()
    if not vaccine:
        raise HTTPException(status_code=404, detail="Vaccine not found")
    for key, value in payload.model_dump().items():
        setattr(vaccine, key, value)
    await db.commit()
    await db.refresh(vaccine)
    return vaccine


@router.delete("/{vaccine_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_vaccine(vaccine_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Vaccine).where(Vaccine.id == vaccine_id))
    vaccine = result.scalar_one_or_none()
    if not vaccine:
        raise HTTPException(status_code=404, detail="Vaccine not found")
    await db.delete(vaccine)
    await db.commit()
