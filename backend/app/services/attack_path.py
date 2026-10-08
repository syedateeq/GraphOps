"""
GraphOps Attack Path Discovery Service.

Given a source node and a target node, finds possible attack paths
through the Neo4j graph using shortest-path algorithms.
Returns structured path information including nodes, relationships,
and a human-readable explanation.
"""

from neo4j.exceptions import ServiceUnavailable

from app.database import db

# Relationship types the attack path traversal will follow.
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

# Map of (source_label, rel_type, direction, target_label) → human description
# direction: "out" means source→target, "in" means target→source
_REL_DESCRIPTIONS = {
    ("User", "USES", "out"): "uses",
    ("Device", "USES", "in"): "is used by",
    ("Device", "HAS_IP", "out"): "has IP address",
    ("Device", "CONNECTED_TO", "out"): "connects to",
    ("Device", "HAS_VULNERABILITY", "out"): "has vulnerability",
    ("Server", "RUNS", "out"): "runs",
    ("Application", "ACCESSES", "out"): "accesses",
    ("Server", "ACCESSES", "out"): "accesses",
    ("User", "PRIVILEGED_ACCESS", "out"): "has privileged access to",
    ("Server", "COMMUNICATES_WITH", "out"): "communicates with",
}


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


def _get_display_name(node_dict: dict) -> str:
    """Return a human-friendly display name for a node."""
    if "name" in node_dict and node_dict["name"]:
        return node_dict["name"]
    if "hostname" in node_dict and node_dict["hostname"]:
        return node_dict["hostname"]
    for key in ("deviceId", "userId", "serverId", "appId", "databaseId", "cveId", "address"):
        if key in node_dict:
            return node_dict[key]
    return "Unknown"


def _get_primary_label(labels: list[str]) -> str:
    """Return the first meaningful label from a node's label list."""
    for label in labels:
        if label in ("User", "Device", "Server", "Application", "Database", "IP", "Vulnerability"):
            return label
    return labels[0] if labels else "Node"


def _build_path_explanation(path_nodes: list[dict], path_rels: list[dict]) -> str:
    """
    Build a human-readable explanation of an attack path.

    Example: "Laptop-07 (Device) →[CONNECTED_TO]→ app-prod-01 (Server) →[ACCESSES]→ Finance-DB (Database)"
    """
    if not path_nodes:
        return ""

    parts = []
    for i, node in enumerate(path_nodes):
        label = _get_primary_label(node["labels"])
        name = _get_display_name(node)
        parts.append(f"{name} ({label})")

        if i < len(path_rels):
            rel = path_rels[i]
            rel_type = rel["type"]
            # Determine direction relative to path order
            if rel["startNodeElementId"] == node["elementId"]:
                parts.append(f" →[{rel_type}]→ ")
            else:
                parts.append(f" ←[{rel_type}]← ")

    return "".join(parts)


def _resolve_node(node_id: str) -> dict | None:
    """
    Find any node in the graph by checking all known ID properties.

    Returns the node dict if found, or None.
    """
    # Try each node type's key property
    checks = [
        ("Device", "deviceId"),
        ("User", "userId"),
        ("Server", "serverId"),
        ("Application", "appId"),
        ("Database", "databaseId"),
        ("Vulnerability", "cveId"),
        ("IP", "address"),
    ]

    with db.get_session() as session:
        for label, prop in checks:
            query = f"MATCH (n:{label} {{{prop}: $nodeId}}) RETURN n LIMIT 1"
            result = session.run(query, nodeId=node_id)
            record = result.single()
            if record:
                return _node_to_dict(record["n"])
    return None


def find_attack_paths(source_id: str, target_id: str, max_paths: int = 5) -> dict:
    """
    Find attack paths between a source node and a target node.

    Uses Neo4j's shortestPath and allShortestPaths to discover
    the shortest and alternative paths through the graph.

    Args:
        source_id: The ID of the source node (e.g. "DEV-007").
        target_id: The ID of the target node (e.g. "DB-001").
        max_paths: Maximum number of alternative paths to return.

    Returns:
        A dict containing source/target info, shortest path,
        all discovered paths, and human-readable explanations.

    Raises:
        ValueError: If source_id or target_id is empty.
        RuntimeError: If the Neo4j driver is not connected.
    """
    if not source_id or not source_id.strip():
        raise ValueError("source_id must not be empty")
    if not target_id or not target_id.strip():
        raise ValueError("target_id must not be empty")

    # Resolve both nodes
    source_node = _resolve_node(source_id)
    if source_node is None:
        return {
            "error": "source_not_found",
            "message": f"No node found with ID '{source_id}'",
        }

    target_node = _resolve_node(target_id)
    if target_node is None:
        return {
            "error": "target_not_found",
            "message": f"No node found with ID '{target_id}'",
        }

    # Build the relationship type filter
    rel_filter = "|".join(TRAVERSAL_REL_TYPES)

    # Find all shortest paths between the two nodes (direction-agnostic)
    # We use element IDs from the resolved nodes for precise matching.
    source_label = _get_primary_label(source_node["labels"])
    target_label = _get_primary_label(target_node["labels"])

    # Determine the key property for each node
    source_key = _get_key_prop(source_label)
    target_key = _get_key_prop(target_label)

    query = f"""
    MATCH (source:{source_label} {{{source_key}: $sourceId}}),
          (target:{target_label} {{{target_key}: $targetId}})
    MATCH path = allShortestPaths((source)-[:{rel_filter} *]-(target))
    RETURN path
    LIMIT $maxPaths
    """

    with db.get_session() as session:
        result = session.run(
            query,
            sourceId=source_id,
            targetId=target_id,
            maxPaths=max_paths,
        )
        records = list(result)

    if not records:
        return {
            "source": source_node,
            "target": target_node,
            "paths_found": 0,
            "message": f"No attack path found between '{source_id}' and '{target_id}'",
            "paths": [],
        }

    # Process all discovered paths
    paths_data = []
    for record in records:
        path = record["path"]
        path_nodes = [_node_to_dict(node) for node in path.nodes]
        path_rels = [_rel_to_dict(rel) for rel in path.relationships]
        explanation = _build_path_explanation(path_nodes, path_rels)

        paths_data.append({
            "hop_count": len(path_rels),
            "nodes": path_nodes,
            "relationships": path_rels,
            "explanation": explanation,
        })

    # Sort by hop count (shortest first)
    paths_data.sort(key=lambda p: p["hop_count"])

    shortest = paths_data[0]

    return {
        "source": source_node,
        "target": target_node,
        "paths_found": len(paths_data),
        "shortest_path": shortest,
        "all_paths": paths_data,
    }


def _get_key_prop(label: str) -> str:
    """Return the key property name for a given node label."""
    mapping = {
        "Device": "deviceId",
        "User": "userId",
        "Server": "serverId",
        "Application": "appId",
        "Database": "databaseId",
        "Vulnerability": "cveId",
        "IP": "address",
    }
    return mapping.get(label, "id")
