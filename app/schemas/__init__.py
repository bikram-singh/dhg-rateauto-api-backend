from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal
from typing import Optional


# ── Department ────────────────────────────────────────────
class DepartmentBase(BaseModel):
    name: str
    description: Optional[str] = None


class DepartmentCreate(DepartmentBase):
    pass


class DepartmentResponse(DepartmentBase):
    id: int
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ── Hospital ──────────────────────────────────────────────
class HospitalBase(BaseModel):
    name: str
    location: Optional[str] = None
    address: Optional[str] = None


class HospitalCreate(HospitalBase):
    pass


class HospitalResponse(HospitalBase):
    id: int
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ── Vaccine ───────────────────────────────────────────────
class VaccineBase(BaseModel):
    name: str
    manufacturer: Optional[str] = None
    description: Optional[str] = None


class VaccineCreate(VaccineBase):
    pass


class VaccineResponse(VaccineBase):
    id: int
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ── Pricing ───────────────────────────────────────────────
class PricingBase(BaseModel):
    vaccine_id: int
    hospital_id: int
    department_id: int
    price: Decimal
    insurance_covered: Optional[str] = "No"
    status: Optional[str] = "Available"


class PricingCreate(PricingBase):
    pass


class PricingUpdate(BaseModel):
    price: Optional[Decimal] = None
    insurance_covered: Optional[str] = None
    status: Optional[str] = None


class PricingResponse(PricingBase):
    id: int
    created_at: Optional[datetime] = None
    vaccine: Optional[VaccineResponse] = None
    hospital: Optional[HospitalResponse] = None
    department: Optional[DepartmentResponse] = None

    class Config:
        from_attributes = True