from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class TicketPriority(str):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class TicketStatus(str):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    CLOSED = "closed"


class SupportTicket(BaseModel):
    id: str
    customer_id: str
    subject: str
    description: str
    priority: str
    status: str
    created_at: datetime
    resolved_at: Optional[datetime] = None


class SupportQueryParams(BaseModel):
    status: Optional[str] = None
    priority: Optional[str] = None
    customer_id: Optional[str] = None
    created_after: Optional[datetime] = None
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=10, ge=1, le=100)
