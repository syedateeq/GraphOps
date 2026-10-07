"""
GraphOps Database Clear Script.

Removes all GraphOps demo nodes and relationships from Neo4j.
"""

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env")

NEO4J_URI = os.getenv("NEO4J_URI", "")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME", "")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "")
NEO4J_DATABASE = os.getenv("NEO4J_DATABASE", "neo4j")

GRAPHOPS_LABELS = [
    "User", "Device", "IP", "Server",
    "Application", "Database", "Vulnerability",
]


def main():
    if not NEO4J_URI or not NEO4J_USERNAME or not NEO4J_PASSWORD:
        print("ERROR: Neo4j credentials not configured.")
        print("Copy backend/.env.example to backend/.env and fill in your credentials.")
        sys.exit(1)

    print(f"Connecting to Neo4j at {NEO4J_URI} ...")
    driver = GraphDatabase.driver(
        NEO4J_URI, auth=(NEO4J_USERNAME, NEO4J_PASSWORD)
    )

    try:
        driver.verify_connectivity()
        print("Connected.\n")

        with driver.session(database=NEO4J_DATABASE) as session:
            for label in GRAPHOPS_LABELS:
                result = session.run(
                    f"MATCH (n:{label}) DETACH DELETE n RETURN count(n) AS deleted"
                )
                deleted = result.single()["deleted"]
                print(f"  Deleted {deleted} {label} node(s).")

        print("\nGraphOps demo data cleared successfully.")

    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)
    finally:
        driver.close()


if __name__ == "__main__":
    main()
