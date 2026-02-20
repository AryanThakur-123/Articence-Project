import json
from pathlib import Path
from typing import List, Dict, Any

from app.connectors.base import BaseConnector
from app.models.common import DataType


DATA_PATH = Path("data/analytics.json")


class AnalyticsConnector(BaseConnector):
    source_name = "analytics"
    data_type = DataType.TIME_SERIES  # default (can change dynamically)

    # -------------------------
    # Data Fetching
    # -------------------------
    def fetch(self, **kwargs) -> List[Dict[str, Any]]:
        """
        Load analytics data from JSON file.
        Expected format:
        [
            {
                "metric_name": "daily_active_users",
                "timestamp": "...",
                "value": 123
            }
        ]
        """
        if not DATA_PATH.exists():
            return []

        with open(DATA_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)

        return data

    # -------------------------
    # Freshness Indicator
    # -------------------------
    def freshness(self) -> str:
        """
        Analytics are usually slightly delayed.
        """
        return "cached_5m"


    # -------------------------
    # Business Rules
    # -------------------------
    def apply_business_rules(
        self,
        data: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        If aggregation requested in filters:
        - Compute total sum
        - Switch data_type to AGGREGATED
        """

        # Detect aggregation request
        if data and all("value" in record for record in data):
            # Keep as time-series by default
            return sorted(
                data,
                key=lambda x: x.get("timestamp", "")
            )

        return data

    # -------------------------
    # Voice Optimization
    # -------------------------
    def build_context(
        self,
        data: List[Dict[str, Any]],
        voice_context: bool
    ) -> str | None:
        if not voice_context:
            return None

        if not data:
            return "No analytics data found for the requested metric."

        metric_name = data[0].get("metric_name", "metric")

        if len(data) == 1:
            value = data[0].get("value", 0)
            return f"The current value of {metric_name} is {value}."

        latest = data[-1].get("value", 0)
        return (
            f"Showing {len(data)} data points for {metric_name}. "
            f"Latest value is {latest}."
        )

    # -------------------------
    # Override Execute for Dynamic DataType
    # -------------------------
    def execute(self, query):
        response = super().execute(query)

        # Detect if aggregated (single computed value scenario)
        if len(response.data) == 1:
            response.metadata.data_type = DataType.AGGREGATED
        else:
            response.metadata.data_type = DataType.TIME_SERIES

        return response
