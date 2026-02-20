import json
from pathlib import Path
from typing import List, Dict, Any

from app.connectors.base import BaseConnector
from app.models.common import DataType


DATA_PATH = Path("data/support_tickets.json")


class SupportConnector(BaseConnector):
    source_name = "support"
    data_type = DataType.TABULAR

    # -------------------------
    # Data Fetching
    # -------------------------
    def fetch(self, **kwargs) -> List[Dict[str, Any]]:
        """
        Load support ticket data from JSON file.
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
        Support systems are typically near real-time.
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
        Business rules:
        - Prioritize open and in_progress tickets
        - Sort by priority (critical > high > medium > low)
        """

        priority_order = {
            "critical": 4,
            "high": 3,
            "medium": 2,
            "low": 1
        }

        # Keep only actionable tickets by default
        actionable_statuses = {"open", "in_progress"}
        filtered = [
            ticket
            for ticket in data
            if ticket.get("status") in actionable_statuses
        ]

        return sorted(
            filtered,
            key=lambda x: priority_order.get(x.get("priority", "low"), 1),
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
            return "There are no open support tickets."

        critical_count = sum(
            1 for ticket in data
            if ticket.get("priority") == "critical"
        )

        return (
            f"There are {len(data)} active support tickets. "
            f"{critical_count} of them are critical priority."
        )
