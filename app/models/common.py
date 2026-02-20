from enum import Enum
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field


class DataSource(str, Enum):
    CRM = "crm"
    SUPPORT = "support"
    ANALYTICS = "analytics"


class DataType(str, Enum):
    TABULAR = "tabular"
    TIME_SERIES = "time_series"
    HIERARCHICAL = "hierarchical"
    AGGREGATED = "aggregated"
    UNKNOWN = "unknown"


class DataQuery(BaseModel):
    source: DataSource = Field(
        ...,
        description="Data source to query: crm | support | analytics"
    )
    filters: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Key-value filters applied to the selected data source"
    )
    limit: int = Field(
        default=10,
        ge=1,
        le=50,
        description="Maximum number of records to return (optimized for voice bandwidth)"
    )
    offset: int = Field(
        default=0,
        ge=0,
        description="Pagination offset"
    )
    voice_context: bool = Field(
        default=True,
        description="Enable voice-optimized summarization"
    )


class Metadata(BaseModel):
    total_results: int = Field(..., ge=0)
    returned_results: int = Field(..., ge=0)
    data_type: DataType = Field(
        ...,
        description="Type of returned data structure"
    )
    freshness: str = Field(
        ...,
        description="Data freshness indicator (e.g., real-time, cached_5m, stale)"
    )
    note: Optional[str] = Field(
        default=None,
        description="Optional business-rule or filtering note"
    )
    summary_hints: Optional[str] = Field(
        default=None,
        description="Optional voice-friendly summary hints"
    )


class DataResponse(BaseModel):
    data: List[Any] = Field(
        ...,
        description="Result set after filtering and pagination"
    )
    metadata: Metadata
    context: Optional[str] = Field(
        default=None,
        description="Concise voice-friendly summary of results"
    )
