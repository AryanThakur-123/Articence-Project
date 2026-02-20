import json
from pathlib import Path
from typing import List, Dict, Any

from app.connectors.base import BaseConnector
from app.models.common import DataType


DATA_PATH = Path("data/customers.json")


class CRMConnector(BaseConnector):
    source_name = "crm"
    data_type = DataType.TABULAR

    # -------------------------
    # Data Fetching
    # -------------------------
    def fetch(self, **kwargs) -> List[Dict[str, Any]]:
        """
        Load CRM customer data from JSON file.
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
        CRM data is typically near real-time.
        """
        return "real-time"

    # -------------------------
    # Business Rules
    # -------------------------
    def apply_business_rules(
        self,
        data: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Example business rules:
        - Exclude churned customers unless explicitly requested
        - Sort by lifetime_value descending
        """

        filtered = [
            customer
            for customer in data
            if customer.get("status") != "churned"
        ]

        return sorted(
            filtered,
            key=lambda x: x.get("lifetime_value", 0),
            reverse=True
        )

    # -------------------------
    # Voice Context Optimization
    # -------------------------
    def build_context(
        self,
        data: List[Dict[str, Any]],
        voice_context: bool
    ) -> str | None:
        if not voice_context:
            return None

        if not data:
            return "No active customers found."

        top_customer = data[0]
        name = top_customer.get("name", "Unknown")
        value = top_customer.get("lifetime_value", 0)

        return (
            f"Showing {len(data)} high-value customers. "
            f"Top customer is {name} with lifetime value {value}."
        )
