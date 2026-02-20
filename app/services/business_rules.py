from typing import List, Dict, Any


class BusinessRulesEngine:
    """
    Centralized business rule processor.
    Keeps domain logic outside connectors.
    """

    @staticmethod
    def apply(source: str, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Apply business rules based on source.
        """

        if not data:
            return data

        if source == "crm":
            return BusinessRulesEngine._crm_rules(data)

        if source == "support":
            return BusinessRulesEngine._support_rules(data)

        if source == "analytics":
            return BusinessRulesEngine._analytics_rules(data)

        return data

    # -------------------------
    # CRM Rules
    # -------------------------
    @staticmethod
    def _crm_rules(data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        # Exclude churned customers
        filtered = [
            customer for customer in data
            if customer.get("status") != "churned"
        ]

        # Sort by lifetime value descending
        return sorted(
            filtered,
            key=lambda x: x.get("lifetime_value", 0),
            reverse=True
        )

    # -------------------------
    # Support Rules
    # -------------------------
    @staticmethod
    def _support_rules(data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        priority_order = {
            "critical": 4,
            "high": 3,
            "medium": 2,
            "low": 1
        }

        actionable_statuses = {"open", "in_progress"}

        filtered = [
            ticket for ticket in data
            if ticket.get("status") in actionable_statuses
        ]

        return sorted(
            filtered,
            key=lambda x: priority_order.get(x.get("priority", "low"), 1),
            reverse=True
        )

    # -------------------------
    # Analytics Rules
    # -------------------------
    @staticmethod
    def _analytics_rules(data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        # Sort by timestamp if exists
        if data and "timestamp" in data[0]:
            return sorted(data, key=lambda x: x.get("timestamp"))

        return data


# from typing import List, Dict


# def apply_business_rules(source: str, data: List[Dict]) -> List[Dict]:
#     """
#     Applies source-specific business filtering and field reduction
#     for voice-friendly output.
#     """

#     if not data:
#         return data

#     if source == "crm":
#         return [
#             {
#                 "id": item.get("id"),
#                 "name": item.get("name"),
#                 "status": item.get("status"),
#                 "last_interaction": item.get("last_interaction"),
#             }
#             for item in data
#         ]

#     if source == "support":
#         return [
#             {
#                 "ticket_id": item.get("ticket_id"),
#                 "priority": item.get("priority"),
#                 "status": item.get("status"),
#                 "created_at": item.get("created_at"),
#             }
#             for item in data
#         ]

#     if source == "analytics":
#         return [
#             {
#                 "metric": item.get("metric"),
#                 "value": item.get("value"),
#                 "timestamp": item.get("timestamp"),
#             }
#             for item in data
#         ]

#     return data
