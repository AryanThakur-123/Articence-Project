from app.services.data_services import fetch_data
from fastapi import APIRouter, Query,Request
from app.models.common import DataResponse, Metadata

router = APIRouter()

@router.get("/data/{source}", response_model=DataResponse)
def get_data(
    source: str,
    request: Request,
    limit: int = Query(10, ge=1),
    offset: int = Query(0, ge=0),
):
    return fetch_data(source, request, limit, offset)

# from fastapi import APIRouter, Query
# from app.connectors.crm_connector import CRMConnector
# from app.connectors.support_connector import SupportConnector
# from app.connectors.analytics_connector import AnalyticsConnector
# from app.services.business_rules import apply_business_rules
# from app.services.voice_optimizer import summarize_if_large
# from app.services.data_identifier import identify_data_type
# from app.models.common import DataResponse, Metadata
# from datetime import datetime

# router = APIRouter()

# @router.get("/data/{source}", response_model=DataResponse)
# def get_data(source: str,limit: int = Query(10, ge=1),offset: int = Query(0, ge=0),status: str | None = None,priority: str | None = None):

#     connector_map = {
#         "crm": CRMConnector(),
#         "support": SupportConnector(),
#         "analytics": AnalyticsConnector(),
#     }

#     connector = connector_map.get(source)
#     if not connector:
#         return {"data": [], "metadata": {"total_results": 0, "returned_results": 0, "data_freshness": "unknown"}}

#     raw_data = connector.fetch()
#     # Filtering
#     if status:
#         raw_data = [item for item in raw_data if item.get("status") == status]

#     if priority:
#         raw_data = [item for item in raw_data if item.get("priority") == priority]
#     total = len(raw_data)

#     paginated = raw_data[offset: offset + limit]

#     filtered = apply_business_rules(source, paginated)
#     optimized = summarize_if_large(filtered)

#     data_type = identify_data_type(raw_data)
#     context = f"Retrieved {len(optimized)} records from {source} source."


#     metadata = Metadata(
#         total_results=total,
#         returned_results=len(optimized),
#         data_type=data_type,
#         freshness=connector.freshness()
#     )

#     return DataResponse(data=optimized, metadata=metadata,context=context)
