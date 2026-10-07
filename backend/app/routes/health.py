"""
GraphOps Health Check Routes.

Provides endpoints for API and Neo4j health monitoring.
"""

from fastapi import APIRouter

from app.database import db

router = APIRouter(prefix="/api/health", tags=["Health"])


@router.get("")
async def health_check():
    """Return basic API health status."""
    return {
        "status": "ok",
        "service": "GraphOps API",
    }


@router.get("/neo4j")
async def neo4j_health():
    """Test Neo4j connection and return database status."""
    result = db.health_check()
    return {
        "service": "Neo4j",
        **result,
    }
