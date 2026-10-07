"""
GraphOps Attack Path Discovery API Routes.

Provides the GET /api/attack-path/{source_id}/{target_id} endpoint.
"""

from fastapi import APIRouter, HTTPException, Query

from app.services.attack_path import find_attack_paths

router = APIRouter(prefix="/api", tags=["Attack Path"])


@router.get("/attack-path/{source_id}/{target_id}")
async def get_attack_path(
    source_id: str,
    target_id: str,
    max_paths: int = Query(
        default=5,
        ge=1,
        le=20,
        description="Maximum number of alternative paths to return. Default is 5.",
    ),
):
    """
    Discover attack paths between a source and target node.

    Given a source node ID (e.g. a compromised Device like "DEV-007")
    and a target node ID (e.g. a critical Database like "DB-001"),
    finds the shortest and alternative attack paths through the graph.

    Node IDs can be any type: deviceId, userId, serverId, appId,
    databaseId, cveId, or IP address.
    """
    try:
        result = find_attack_paths(source_id, target_id, max_paths=max_paths)
    except RuntimeError:
        raise HTTPException(
            status_code=503,
            detail="Neo4j database is not available. Check the connection.",
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis error: {str(e)}")

    # If the service returned an error dict (node not found)
    if "error" in result:
        if result["error"] in ("source_not_found", "target_not_found"):
            raise HTTPException(status_code=404, detail=result["message"])
        raise HTTPException(status_code=400, detail=result["message"])

    return result
