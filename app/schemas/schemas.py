from datetime import datetime
from typing import List

from pydantic.main import BaseModel


class CpuPerformance(BaseModel):
    id: int
    performance: float
    date_time: datetime


class CpuPerformanceAll(BaseModel):
    id: int
    performance: float
    average_performance: float
    date_time: datetime = None


class CpuPerformanceCreate(BaseModel):
    performance: float
