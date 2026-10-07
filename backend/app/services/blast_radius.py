"""
GraphOps Blast Radius Analysis Service.

Given a compromised device, uses Neo4j graph traversal to find
all assets reachable within a configurable hop limit. Returns
structured node and relationship data organized by hop distance.
"""

from neo4j.exceptions import ServiceUnavailable

from app.database import db

# Maximum allowed hop depth to prevent runaway traversals
MAX_HOP_LIMIT = 10

# Relationship types the blast radius traversal will follow.
# These are ALL directed relationships in the seed schema.
# We traverse them in any direction so lateral movement is captured.
TRAVERSAL_REL_TYPES = [
    "USES",
    "HAS_IP",
    "CONNECTED_TO",
    "RUNS",
    "ACCESSES",
    "HAS_VULNERABILITY",
    "PRIVILEGED_ACCESS",
    "COMMUNICATES_WITH",
]


def _node_to_dict(node) -> dict:
    """Convert a Neo4j node to a serialisable dict with id and labels."""
    props = dict(node)
    return {
        "elementId": node.element_id,
        "labels": list(node.labels),
        **props,
    }


def _rel_to_dict(rel) -> dict:
    """Convert a Neo4j relationship to a serialisable dict."""
    return {
        "elementId": rel.element_id,
        "type": rel.type,
        "startNodeElementId": rel.start_node.element_id,
        "endNodeElementId": rel.end_node.element_id,
        **dict(rel),
    }


def _get_node_type_id(node_dict: dict) -> str:
    """Return the primary ID value for a node (e.g. deviceId, userId)."""
    for key in ("deviceId", "userId", "serverId", "appId", "databaseId", "cveId", "address"):
        if key in node_dict:
            return node_dict[key]
    return node_dict.get("elementId", "unknown")


def _classify_label(labels: list[str]) -> str:
    """Return a lowercase label category from a node's label list."""
    for label in labels:
        low = label.lower()
        if low in ("user", "device", "server", "application", "database", "ip", "vulnerability"):
            return low
    return "other"


def validate_device_exists(device_id: str) -> dict | None:
    """
    Check whether a Device node with the given deviceId exists.

    Returns the node dict if found, or None.
    """
    query = "MATCH (d:Device {deviceId: $deviceId}) RETURN d LIMIT 1"
    try:
        with db.get_session() as session:
            result = session.run(query, deviceId=device_id)
            record = result.single()
            if record:
                return _node_to_dict(record["d"])
    except (RuntimeError, ServiceUnavailable):
        raise
    return None


def compute_blast_radius(device_id: str, max_hops: int = 3) -> dict:
    """
    Compute the blast radius from a compromised device.

    Uses a variable-length path query to discover all nodes
    reachable within ``max_hops`` hops, then groups them by
    hop distance.

    Args:
        device_id: The deviceId of the compromised device.
        max_hops: Maximum traversal depth (1–MAX_HOP_LIMIT).

    Returns:
        A dict containing the compromised device, nodes per hop,
        affected asset counts, critical assets, and relationships.

    Raises:
        ValueError: If device_id is empty or max_hops is invalid.
        RuntimeError: If the Neo4j driver is not connected.
    """
    if not device_id or not device_id.strip():
        raise ValueError("device_id must not be empty")
    max_hops = max(1, min(max_hops, MAX_HOP_LIMIT))

    # Build the relationship type filter string for Cypher
    rel_filter = "|".join(TRAVERSAL_REL_TYPES)

    # Variable-length path: find every distinct node reachable from the device
    # within 1..max_hops hops, following any of the listed relationship types
    # in either direction.
    query = f"""
    MATCH (start:Device {{deviceId: $deviceId}})
    MATCH path = (start)-[:{rel_filter} *1..{max_hops}]-(reached)
    WHERE start <> reached
    WITH reached,
         min(length(path)) AS hopDistance,
         collect(DISTINCT path) AS paths
    RETURN reached, hopDistance, paths
    ORDER BY hopDistance
    """

    with db.get_session() as session:
        result = session.run(query, deviceId=device_id)
        records = list(result)

    # Organise results by hop distance
    nodes_by_hop: dict[int, list[dict]] = {hop: [] for hop in range(1, max_hops + 1)}
    all_nodes: dict[str, dict] = {}  # element_id → node dict  (dedup)
    all_rels: dict[str, dict] = {}   # element_id → rel dict   (dedup)

    for record in records:
        node = record["reached"]
        hop = record["hopDistance"]
        node_dict = _node_to_dict(node)
        eid = node_dict["elementId"]

        if eid not in all_nodes:
            all_nodes[eid] = node_dict
            bucket = min(hop, max_hops)
            nodes_by_hop.setdefault(bucket, []).append(node_dict)

        # Extract relationships from every path for this node
        for path in record["paths"]:
            for rel in path.relationships:
                rel_eid = rel.element_id
                if rel_eid not in all_rels:
                    all_rels[rel_eid] = _rel_to_dict(rel)

    # Count affected assets by type
    counts: dict[str, int] = {
        "users": 0,
        "devices": 0,
        "servers": 0,
        "applications": 0,
        "databases": 0,
        "ips": 0,
        "vulnerabilities": 0,
    }
    critical_assets: list[dict] = []

    for nd in all_nodes.values():
        cat = _classify_label(nd["labels"])
        key = cat + "s" if cat != "vulnerability" else "vulnerabilities"
        if key in counts:
            counts[key] += 1
        # Mark critical assets
        if nd.get("criticality") in ("critical", "high"):
            critical_assets.append({
                "id": _get_node_type_id(nd),
                "labels": nd["labels"],
                "name": nd.get("name") or nd.get("hostname") or _get_node_type_id(nd),
                "criticality": nd.get("criticality"),
            })

    return {
        "compromised_device": device_id,
        "max_hops": max_hops,
        "hop_1_nodes": nodes_by_hop.get(1, []),
        "hop_2_nodes": nodes_by_hop.get(2, []),
        "hop_3_nodes": nodes_by_hop.get(3, []),
        "nodes_by_hop": {str(k): v for k, v in nodes_by_hop.items()},
        "total_affected_assets": len(all_nodes),
        "affected_counts": counts,
        "critical_assets": critical_assets,
        "relationships": list(all_rels.values()),
        "all_nodes": list(all_nodes.values()),
    }
