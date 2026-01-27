"""
Database service abstract base class.
Based on db-chat-nl database_base.py
"""
from abc import ABC, abstractmethod
from typing import Dict, List, Any


class DatabaseService(ABC):
    """
    Abstract base class for database adapters.
    Provides interface for schema introspection and query execution.
    """

    @abstractmethod
    def get_schema(self) -> Dict[str, Any]:
        """
        Get database schema information.

        Returns:
            Dict containing tables and their columns
        """
        pass

    @abstractmethod
    def execute_query(self, sql: str) -> List[Dict[str, Any]]:
        """
        Execute SQL query and return results.

        Args:
            sql: SQL query string (SELECT only)

        Returns:
            List of row dictionaries
        """
        pass

    def test_connection(self) -> bool:
        """
        Test database connectivity.

        Returns:
            True if connection successful
        """
        return True


class DatabaseServiceStub(DatabaseService):
    """Stub implementation for testing and scaffolding."""

    def get_schema(self) -> Dict[str, Any]:
        return {"tables": []}

    def execute_query(self, sql: str) -> List[Dict[str, Any]]:
        return []
