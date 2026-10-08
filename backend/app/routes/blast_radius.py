"""
GraphOps Blast Radius API Routes.

Provides the GET /api/blast-radius/{device_id} endpoint.
"""

from fastapi import APIRouter, HTTPException, Query

from app.services.blast_radius import (
    compute_blast_radius,
    validate_device_exists,
    MAX_HOP_LIMIT,
)

router = APIRouter(prefix="/api", tags=["Blast Radius"])


@router.get("/blast-radius/{device_id}")
async def get_blast_radius(
    device_id: str,
    max_hops: int = Query(
        default=3,
        ge=1,
        le=MAX_HOP_LIMIT,
        description="Maximum traversal depth (1–10). Default is 3.",
    ),
):
    """
    Compute the blast radius from a compromised device.

    Given a Device ID, traverses the Neo4j graph to find all assets
    reachable within the specified hop limit. Returns nodes grouped
    by hop distance, affected asset counts, critical assets, and
    the relationships used to reach them.
    """
    # Validate the device exists
    try:
        device = validate_device_exists(device_id)
    except RuntimeError:
        raise HTTPException(
            status_code=503,
            detail="Neo4j database is not available. Check the connection.",
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    if device is None:
        raise HTTPException(
            status_code=404,
            detail=f"Device '{device_id}' not found in the graph.",
        )

    # Compute the blast radius
    try:
        result = compute_blast_radius(device_id, max_hops=max_hops)
    except RuntimeError:
        raise HTTPException(
            status_code=503,
            detail="Neo4j database is not available. Check the connection.",
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis error: {str(e)}")

    return result
