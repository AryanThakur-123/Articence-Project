from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class MetricPoint(BaseModel):
    timestamp: datetime
    value: float


class TimeSeriesMetric(BaseModel):
    metric_name: str
    points: List[MetricPoint]


class AggregatedMetric(BaseModel):
    metric_name: str
    value: float
    period: str  # e.g., "last_7_days"


class AnalyticsQueryParams(BaseModel):
    metric_name: str
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    aggregate: bool = False
