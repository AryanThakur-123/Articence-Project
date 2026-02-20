from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class CustomerStatus(str):
    ACTIVE = "active"
    INACTIVE = "inactive"
    CHURNED = "churned"


class Customer(BaseModel):
    id: str
    name: str
    email: str
    company: Optional[str] = None
    status: str
    lifetime_value: float = Field(ge=0)
    created_at: datetime
    last_activity_at: Optional[datetime] = None


class CRMQueryParams(BaseModel):
    status: Optional[str] = None
    min_lifetime_value: Optional[float] = Field(default=None, ge=0)
    created_after: Optional[datetime] = None
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=10, ge=1, le=100)
