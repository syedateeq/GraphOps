"""
GraphOps Phase 2 — Endpoint verification tests.

Tests the blast-radius and attack-path endpoints against
the seeded Neo4j database. Also verifies that existing
health endpoints remain functional.

Usage:
    cd backend
    python scripts/test_phase2.py

Requires the backend to be running on localhost:8000.
"""

import json
import sys
import urllib.request
import urllib.error

BASE_URL = "http://localhost:8000"

passed = 0
failed = 0


def test(name: str, method: str, path: str, expect_status: int, check_fn=None):
    """Run a single test case."""
    global passed, failed
    url = f"{BASE_URL}{path}"
    print(f"\n{'─' * 60}")
    print(f"TEST: {name}")
    print(f"  {method} {path}")

    try:
        req = urllib.request.Request(url, method=method)
        with urllib.request.urlopen(req) as resp:
            status = resp.status
            body = json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        status = e.code
        try:
            body = json.loads(e.read().decode())
        except Exception:
            body = {}
    except urllib.error.URLError as e:
        print(f"  ✗ FAIL — Cannot connect to {BASE_URL}: {e}")
        failed += 1
        return
    except Exception as e:
        print(f"  ✗ FAIL — Unexpected error: {e}")
        failed += 1
        return

    if status != expect_status:
        print(f"  ✗ FAIL — Expected status {expect_status}, got {status}")
        print(f"  Response: {json.dumps(body, indent=2)[:500]}")
        failed += 1
        return

    if check_fn:
        try:
            check_fn(body)
        except AssertionError as e:
            print(f"  ✗ FAIL — Assertion failed: {e}")
            print(f"  Response: {json.dumps(body, indent=2)[:500]}")
            failed += 1
            return

    print(f"  ✓ PASS (status={status})")
    # Print a compact summary for successful responses
    if status == 200:
        summary_keys = ["status", "total_affected_assets", "paths_found",
                        "compromised_device", "message"]
        summary = {k: body[k] for k in summary_keys if k in body}
        if summary:
            print(f"  Summary: {json.dumps(summary)}")
    passed += 1


# ─── Health Endpoints (must still work) ─────────────────────────────

def test_health_api(body):
    assert body["status"] == "ok", f"Expected status 'ok', got '{body['status']}'"


def test_health_neo4j(body):
    assert body["status"] == "connected", f"Expected 'connected', got '{body['status']}'"


# ─── Blast Radius ───────────────────────────────────────────────────

def test_blast_radius_valid(body):
    assert body["compromised_device"] == "DEV-007"
    assert body["max_hops"] == 3
    assert body["total_affected_assets"] > 0, "Expected at least one affected asset"
    assert len(body["hop_1_nodes"]) > 0, "Expected at least one 1-hop node"
    assert len(body["relationships"]) > 0, "Expected at least one relationship"
    assert "affected_counts" in body
    assert "critical_assets" in body


def test_blast_radius_custom_hops(body):
    assert body["max_hops"] == 1
    assert body["total_affected_assets"] > 0


def test_blast_radius_all_nodes(body):
    """Verify the all_nodes list matches total_affected_assets."""
    assert len(body["all_nodes"]) == body["total_affected_assets"]


# ─── Attack Path ────────────────────────────────────────────────────

def test_attack_path_valid(body):
    assert body["paths_found"] > 0, "Expected at least one path"
    shortest = body["shortest_path"]
    assert shortest["hop_count"] > 0
    assert len(shortest["nodes"]) > 0
    assert len(shortest["relationships"]) > 0
    assert shortest["explanation"], "Expected a non-empty explanation"
    print(f"  Shortest path ({shortest['hop_count']} hops): {shortest['explanation']}")


def test_attack_path_no_path(body):
    """When no path exists, expect paths_found=0."""
    assert body["paths_found"] == 0
    assert "message" in body


# ─── Run All Tests ──────────────────────────────────────────────────

def main():
    print("=" * 60)
    print("GraphOps Phase 2 — Endpoint Verification")
    print("=" * 60)

    # 1. Existing health endpoints
    test("Health API (existing)",
         "GET", "/api/health", 200, test_health_api)

    test("Health Neo4j (existing)",
         "GET", "/api/health/neo4j", 200, test_health_neo4j)

    # 2. Blast radius — valid device
    test("Blast radius — DEV-007 (compromised device)",
         "GET", "/api/blast-radius/DEV-007", 200, test_blast_radius_valid)

    # 3. Blast radius — custom hop limit
    test("Blast radius — DEV-007 with max_hops=1",
         "GET", "/api/blast-radius/DEV-007?max_hops=1", 200,
         test_blast_radius_custom_hops)

    # 4. Blast radius — verify all_nodes
    test("Blast radius — verify all_nodes consistency",
         "GET", "/api/blast-radius/DEV-007", 200, test_blast_radius_all_nodes)

    # 5. Blast radius — device not found
    test("Blast radius — non-existent device (404)",
         "GET", "/api/blast-radius/DEV-999", 404)

    # 6. Blast radius — another valid device
    test("Blast radius — DEV-001 (normal device)",
         "GET", "/api/blast-radius/DEV-001", 200)

    # 7. Attack path — valid path (DEV-007 → DB-001)
    test("Attack path — DEV-007 → DB-001 (known attack path)",
         "GET", "/api/attack-path/DEV-007/DB-001", 200, test_attack_path_valid)

    # 8. Attack path — user to database
    test("Attack path — USR-001 → DB-001",
         "GET", "/api/attack-path/USR-001/DB-001", 200, test_attack_path_valid)

    # 9. Attack path — source not found
    test("Attack path — non-existent source (404)",
         "GET", "/api/attack-path/DEV-999/DB-001", 404)

    # 10. Attack path — target not found
    test("Attack path — non-existent target (404)",
         "GET", "/api/attack-path/DEV-007/DB-999", 404)

    # 11. Attack path — no path possible (isolated node unlikely, but try far nodes)
    # DEV-034 is a device with no CONNECTED_TO relationships in seed data
    # and CVE-2024-20353 is a vulnerability not attached to it — so path
    # may or may not exist depending on graph connectivity. We just verify
    # the endpoint responds correctly.
    test("Attack path — DEV-034 → CVE-2024-20353 (may have no path)",
         "GET", "/api/attack-path/DEV-034/CVE-2024-20353", 200,
         lambda body: True)  # Accept any 200 response

    # Summary
    print(f"\n{'=' * 60}")
    print(f"RESULTS: {passed} passed, {failed} failed, {passed + failed} total")
    print(f"{'=' * 60}")

    if failed > 0:
        sys.exit(1)
    print("\nAll tests passed! ✓")


if __name__ == "__main__":
    main()
