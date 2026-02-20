from abc import ABC, abstractmethod
from typing import List, Dict, Any, Type
from app.models.common import DataQuery, DataResponse, Metadata, DataType
from app.services.data_identifier import identify_data_type
from app.services.business_rules import BusinessRulesEngine
from app.services.voice_optimizer import VoiceOptimizer

import logging

logger = logging.getLogger(__name__)


class BaseConnector(ABC):
    """
    Abstract base connector enforcing a unified contract
    across all data sources (CRM, Support, Analytics).
    """

    source_name: str
    data_type: DataType

    # -------------------------
    # Core Data Retrieval
    # -------------------------
    @abstractmethod
    def fetch(self, **kwargs) -> List[Dict[str, Any]]:
        """
        Fetch raw data from the underlying data source.
        Must return a list of dictionaries.
        """
        pass

    # -------------------------
    # Freshness Indicator
    # -------------------------
    @abstractmethod
    def freshness(self) -> str:
        """
        Return freshness indicator string.
        Example: 'real-time', 'cached_5m', 'stale'
        """
        pass

    # -------------------------
    # Optional Hook: Filtering
    # -------------------------
    def apply_filters(
        self,
        data: List[Dict[str, Any]],
        filters: Dict[str, Any] | None,
    ) -> List[Dict[str, Any]]:

        if not filters:
            return data

        filtered = []

        for item in data:
            keep = True

            for key, value in filters.items():

                # Handle operators like value__gt
                if "__" in key:
                    field, op = key.split("__", 1)
                    item_value = item.get(field)

                    if item_value is None:
                        keep = False
                        break

                    # 🔥 Force numeric comparison when possible
                    try:
                        item_value = float(item_value)
                        value = float(value)
                    except (ValueError, TypeError):
                        keep = False
                        break

                    if op == "gt" and not (item_value > value):
                        keep = False
                        break
                    elif op == "lt" and not (item_value < value):
                        keep = False
                        break
                    elif op == "gte" and not (item_value >= value):
                        keep = False
                        break
                    elif op == "lte" and not (item_value <= value):
                        keep = False
                        break

                # Handle equality
                else:
                    if str(item.get(key)) != str(value):
                        keep = False
                        break

            if keep:
                filtered.append(item)

        return filtered




    # -------------------------
    # Optional Hook: Business Rules
    # -------------------------
    def apply_business_rules(
        self,
        data: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Override in child connectors if business logic
        filtering is required.
        """
        return data

    # -------------------------
    # Pagination / Limiting
    # -------------------------
    def limit_results(
        self,
        data: List[Dict[str, Any]],
        limit: int,
        offset: int
    ) -> List[Dict[str, Any]]:
        return data[offset: offset + limit]

    # -------------------------
    # Unified Execution Method
    # -------------------------
    def execute(self, query: DataQuery) -> DataResponse:
        """
        Full pipeline execution:
        1. Fetch raw data
        2. Apply filters
        3. Apply business rules
        4. Apply pagination
        5. Apply voice optimization
        6. Construct standardized response
        """

        logger.info("Fetching data using %s", self.__class__.__name__)
        logger.info("Query filters: %s", query.filters)

        # 1. Fetch
        raw_data = self.fetch()
        total_results = len(raw_data)

        logger.info("Raw data fetched. Total records: %d", total_results)

        # 2. Apply filters
        filtered_data = self.apply_filters(raw_data, query.filters)

        logger.info("Filtered records count: %d", len(filtered_data))

        # 3. Apply business rules
        filtered_data = BusinessRulesEngine.apply(
            query.source,
            filtered_data
        )

        logger.info("After business rules count: %d", len(filtered_data))

        # 4. Pagination
        limited_data = self.limit_results(
            filtered_data,
            query.limit,
            query.offset
        )

        logger.info(
            "After pagination → offset=%d limit=%d returned=%d",
            query.offset,
            query.limit,
            len(limited_data)
        )

        # 5. Voice optimization
        if query.voice_context:
            logger.info("Applying voice optimization")
            limited_data, context = VoiceOptimizer.optimize(
                query.source,
                limited_data
            )
        else:
            context = None

        # 6. Build metadata
        metadata = Metadata(
            total_results=total_results,
            returned_results=len(limited_data),
            data_type=identify_data_type(limited_data),
            freshness=self.freshness(),
            note=None,
            summary_hint="Use context field to generate concise answer."
        )

        logger.info("Connector execution completed successfully")

        return DataResponse(
            data=limited_data,
            metadata=metadata,
            context=context
        )