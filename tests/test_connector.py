from app.connectors.analytics_connector import AnalyticsConnector
from app.connectors.crm_connector import CRMConnector
from app.connectors.support_connector import SupportConnector


def test_analytics_connector_fetch():
    connector = AnalyticsConnector()
    data = connector.fetch()

    assert isinstance(data, list)
    assert len(data) > 0
    assert isinstance(data[0], dict)


def test_crm_connector_fetch():
    connector = CRMConnector()
    data = connector.fetch()

    assert isinstance(data, list)
    assert len(data) > 0
    assert isinstance(data[0], dict)


def test_support_connector_fetch():
    connector = SupportConnector()
    data = connector.fetch()

    assert isinstance(data, list)
    assert len(data) > 0
    assert isinstance(data[0], dict)