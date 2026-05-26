from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Pricing(Base):
    __tablename__ = "pricing"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True)
    vaccine_id = Column(Integer, ForeignKey("vaccines.id"), nullable=False)
    hospital_id = Column(Integer, ForeignKey("hospitals.id"), nullable=False)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    insurance_covered = Column(String(20), default="No")
    status = Column(String(20), default="Available")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    vaccine = relationship("app.models.vaccine.Vaccine", back_populates="pricing")
    hospital = relationship("app.models.hospital.Hospital", back_populates="pricing")
    department = relationship("app.models.department.Department", back_populates="pricing")
