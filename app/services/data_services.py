from typing import Dict, Any

from fastapi import HTTPException, Request

from app.models.common import DataQuery
from app.connectors.crm_connector import CRMConnector
from app.connectors.support_connector import SupportConnector
from app.connectors.analytics_connector import AnalyticsConnector


# -------------------------
# Connector Registry
# -------------------------

CONNECTOR_REGISTRY = {
    "crm": CRMConnector(),
    "support": SupportConnector(),
    "analytics": AnalyticsConnector(),
}


# -------------------------
# Fetch Data Service
# -------------------------

def fetch_data(
    source: str,
    request: Request,
    limit: int,
    offset: int,
):
    connector = CONNECTOR_REGISTRY.get(source)

    if not connector:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported data source: {source}"
        )

    # Extract dynamic query params
    raw_params = dict(request.query_params)

    # Remove pagination params
    raw_params.pop("limit", None)
    raw_params.pop("offset", None)

    query = DataQuery(
        source=source,
        filters=raw_params if raw_params else None,
        limit=limit,
        offset=offset,
        voice_context=True
    )

    return connector.execute(query)




# from app.connectors.crm_connector import CRMConnector
# from app.connectors.support_connector import SupportConnector
# from app.connectors.analytics_connector import AnalyticsConnector
# from app.services.business_rules import apply_business_rules
# from app.services.voice_optimizer import summarize_if_large
# from app.services.data_identifier import identify_data_type
# from app.models.common import DataResponse, Metadata
# import logging

# logger = logging.getLogger(__name__)


# def fetch_data(source: str, limit: int = 10, offset: int = 0, status: str | None = None, priority: str | None = None):

#     logger.info(f"Fetching data from source: {source}")

#     if status:
#         logger.info(f"Applying status filter: {status}")

#     if priority:
#         logger.info(f"Applying priority filter: {priority}")

#     logger.info(f"Returning {len(optimized)} records")


#     connector_map = {
#         "crm": CRMConnector(),
#         "support": SupportConnector(),
#         "analytics": AnalyticsConnector(),
#     }

#     connector = connector_map.get(source)
#     if not connector:
#         return DataResponse(
#             data=[],
#             metadata=Metadata(
#                 total_results=0,
#                 returned_results=0,
#                 data_type="unknown",
#                 freshness="unknown"
#             ),
#             context="Invalid data source."
#         )

#     raw_data = connector.fetch()

#     if status:
#         raw_data = [item for item in raw_data if item.get("status") == status]

#     if priority:
#         raw_data = [item for item in raw_data if item.get("priority") == priority]

#     total = len(raw_data)

#     paginated = raw_data[offset: offset + limit]
#     filtered = apply_business_rules(source, paginated)
#     optimized = summarize_if_large(filtered)

#     data_type = identify_data_type(raw_data)

#     metadata = Metadata(
#         total_results=total,
#         returned_results=len([i for i in optimized if "note" not in i]),
#         data_type=data_type,
#         freshness=connector.freshness()
#     )

#     context = f"Retrieved {len(optimized)} records from {source} source."

#     return DataResponse(data=optimized, metadata=metadata, context=context)
