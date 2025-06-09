# Database models using SQLAlchemy

from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean
from sqlalchemy.sql import func
from .db import Base

class ResourceScan(Base):
    __tablename__ = "resource_scans"

    id = Column(Integer, primary_key=True, index=True)
    resource_name = Column(String, index=True)
    resource_type = Column(String)
    average_cpu = Column(Float)
    region = Column(String)
    cloud_provider = Column(String)
    detected_at = Column(DateTime(timezone=True), server_default=func.now())

class CostRecommendation(Base):
    __tablename__ = "cost_recommendations"

    id = Column(Integer, primary_key=True, index=True)
    resource_name = Column(String, index=True)
    recommendation = Column(String)
    summary = Column(String)
    estimated_savings = Column(Float)
    applied = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
