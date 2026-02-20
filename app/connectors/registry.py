from app.connectors.crm_connector import CRMConnector
from app.connectors.support_connector import SupportConnector
from app.connectors.analytics_connector import AnalyticsConnector


CONNECTOR_MAP = {
    "crm": CRMConnector(),
    "support": SupportConnector(),
    "analytics": AnalyticsConnector()
}


def get_connector(source: str):
    if source not in CONNECTOR_MAP:
        raise ValueError(f"Unknown data source: {source}")
    return CONNECTOR_MAP[source]
