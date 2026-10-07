"""
GraphOps Neo4j Database Service.

Provides a reusable Neo4j driver with connection management and health checking.
"""

from neo4j import GraphDatabase
from neo4j.exceptions import ServiceUnavailable, AuthError

from app.config import neo4j_settings


class Neo4jConnection:
    """Manages the Neo4j driver lifecycle."""

    def __init__(self):
        self._driver = None

    def connect(self) -> None:
        """Initialize the Neo4j driver using settings from environment variables."""
        if not neo4j_settings.validate_credentials():
            print(
                "WARNING: Neo4j credentials not fully configured. "
                "Set NEO4J_URI, NEO4J_USERNAME, and NEO4J_PASSWORD in your .env file."
            )
            return

        try:
            self._driver = GraphDatabase.driver(
                neo4j_settings.uri,
                auth=(neo4j_settings.username, neo4j_settings.password),
            )
            # Verify connectivity
            self._driver.verify_connectivity()
            print(f"Connected to Neo4j at {neo4j_settings.uri}")
        except AuthError:
            print("ERROR: Neo4j authentication failed. Check your credentials.")
            self._driver = None
        except ServiceUnavailable:
            print(
                f"ERROR: Cannot reach Neo4j at {neo4j_settings.uri}. "
                "Is the database running?"
            )
            self._driver = None
        except Exception as e:
            print(f"ERROR: Failed to connect to Neo4j: {e}")
            self._driver = None

    def close(self) -> None:
        """Close the Neo4j driver."""
        if self._driver:
            self._driver.close()
            self._driver = None
            print("Neo4j connection closed.")

    @property
    def driver(self):
        """Return the Neo4j driver instance."""
        return self._driver

    def get_session(self, **kwargs):
        """
        Create and return a new Neo4j session.

        Raises RuntimeError if the driver is not connected.
        """
        if not self._driver:
            raise RuntimeError(
                "Neo4j driver is not connected. "
                "Check your credentials and database status."
            )
        return self._driver.session(
            database=neo4j_settings.database, **kwargs
        )

    def health_check(self) -> dict:
        """
        Test Neo4j connectivity and return a status dict.

        Returns:
            dict with status, message, and optional details.
        """
        if not neo4j_settings.validate_credentials():
            return {
                "status": "error",
                "message": "Neo4j credentials not configured",
            }

        if not self._driver:
            return {
                "status": "error",
                "message": "Neo4j driver not initialized",
            }

        try:
            with self.get_session() as session:
                result = session.run("RETURN 1 AS ok")
                record = result.single()
                if record and record["ok"] == 1:
                    return {
                        "status": "connected",
                        "message": "Neo4j is reachable",
                        "uri": neo4j_settings.uri,
                        "database": neo4j_settings.database,
                    }
            return {"status": "error", "message": "Unexpected query result"}
        except Exception as e:
            return {"status": "error", "message": str(e)}


# Singleton instance
db = Neo4jConnection()
