# GraphOps

**Cybersecurity Graph Intelligence Platform**

GraphOps is a threat-hunting and blast-radius analysis platform built around a Neo4j security knowledge graph. It helps security analysts understand the connected environment when a device is compromised — discovering attack paths, mapping blast radius, identifying choke-point nodes, and recommending containment actions.

> **Current status: Phase 3 — SOC Dashboard + Interactive Graph Visualization**

---

## Architecture

```
React + Vite  ───►  FastAPI + Uvicorn  ───►  Neo4j (AuraDB compatible)
  (5173)                (8000)                     (7687)
```

See [`docs/architecture.md`](docs/architecture.md) for the full architecture reference, graph schema, and attack scenario details.

---

## Technology Stack

| Layer    | Technology                      |
|----------|---------------------------------|
| Backend  | Python 3.11+, FastAPI, Uvicorn  |
| Frontend | React, Vite, TypeScript         |
| Database | Neo4j (local or AuraDB)         |
| Driver   | neo4j Python driver             |
| Config   | python-dotenv, Pydantic         |

---

## Folder Structure

```
graphops/
├── backend/
│   ├── app/
│   │   ├── main.py                    # FastAPI app
│   │   ├── config.py                  # Settings from env vars
│   │   ├── database.py                # Neo4j connection service
│   │   ├── routes/
│   │   │   ├── health.py              # Health-check endpoints
│   │   │   ├── blast_radius.py        # Blast radius analysis endpoint
│   │   │   └── attack_path.py         # Attack path discovery endpoint
│   │   └── services/
│   │       ├── blast_radius.py        # Blast radius graph traversal logic
│   │       └── attack_path.py         # Attack path discovery logic
│   ├── scripts/
│   │   ├── seed_database.py           # Populate Neo4j with demo data
│   │   ├── clear_database.py          # Clear demo data
│   │   └── test_phase2.py             # Phase 2 endpoint verification
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── App.tsx                    # Status dashboard
│   │   ├── main.tsx                   # React entry point
│   │   ├── index.css                  # Styles
│   │   └── services/api.ts           # API client
│   ├── package.json
│   └── .env.example
├── data/                              # Data exports (gitignored)
├── docs/architecture.md               # Architecture docs
├── .gitignore
└── README.md
```

---

## Prerequisites

- **Python 3.11+** — [python.org](https://www.python.org/downloads/)
- **Node.js 18+** — [nodejs.org](https://nodejs.org/)
- **Neo4j** — either:
  - [Neo4j Desktop](https://neo4j.com/download/) (local)
  - [Neo4j AuraDB](https://neo4j.com/cloud/aura/) (free-tier cloud)

---

## Neo4j Setup

### Option A: Neo4j AuraDB (recommended for quick start)

1. Go to [Neo4j AuraDB](https://neo4j.com/cloud/aura/) and create a free instance.
2. Note the **connection URI** (e.g. `neo4j+s://xxxxxxxx.databases.neo4j.io`), **username**, and **password**.

### Option B: Neo4j Desktop (local)

1. Download and install [Neo4j Desktop](https://neo4j.com/download/).
2. Create a new project and a local DBMS.
3. Start the DBMS. The default URI is `bolt://localhost:7687`.

---

## Backend Setup

Open PowerShell and run:

```powershell
# Navigate to the backend directory
cd graphops\backend

# Create a virtual environment
python -m venv venv

# Activate it
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Create your .env file from the example
Copy-Item .env.example .env

# Edit .env with your Neo4j credentials
notepad .env
```

Edit `.env` and fill in your Neo4j credentials:

```
NEO4J_URI=neo4j+s://your-instance.databases.neo4j.io
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=your_actual_password
NEO4J_DATABASE=neo4j
```

Start the backend:

```powershell
uvicorn app.main:app --reload --port 8000
```

---

## Frontend Setup

Open a **second PowerShell** window:

```powershell
# Navigate to the frontend directory
cd graphops\frontend

# Install dependencies (already done if you followed the steps above)
npm install

# Start the dev server
npm run dev
```

The frontend will be available at **http://localhost:5173**.

---

## Seeding the Database

With the virtual environment activated:

```powershell
cd graphops\backend
python scripts/seed_database.py
```

Expected output:

```
Connecting to Neo4j at neo4j+s://... ...
Connected.

Creating constraints ...
  Constraints created.
Seeding nodes ...
  Nodes created.
Seeding relationships ...
  Relationships created: 134

  === GraphOps Database Statistics ===

  Users:              25
  Devices:            40
  IPs:                20
  Servers:            15
  Applications:       10
  Databases:          8
  Vulnerabilities:    15

  Relationships:      134

GraphOps database seeded successfully.
```

The script uses `MERGE` — running it multiple times will **not** create duplicates.

---

## Clearing the Database

To remove all GraphOps demo data:

```powershell
cd graphops\backend
python scripts/clear_database.py
```

This only deletes nodes with GraphOps labels (User, Device, Server, etc.) and their relationships.

---

## API Endpoints

### Health Checks

| Endpoint               | Description                |
|------------------------|----------------------------|
| `GET /api/health`      | API liveness check         |
| `GET /api/health/neo4j`| Neo4j connectivity test    |

### Phase 2 — Graph Intelligence

| Endpoint                                      | Description                              |
|-----------------------------------------------|------------------------------------------|
| `GET /api/blast-radius/{device_id}`           | Blast radius analysis from a device      |
| `GET /api/attack-path/{source_id}/{target_id}`| Attack path discovery between two nodes  |

---

## Blast Radius Analysis

**Endpoint:** `GET /api/blast-radius/{device_id}`

Given a compromised device, uses Neo4j variable-length path traversal to find all assets reachable within a configurable hop limit. Traverses all relationship types in either direction to capture lateral movement paths.

**Query parameter:**
- `max_hops` (int, default: 3, range: 1–10) — maximum traversal depth

**How it works:**

1. Validates the device exists in the graph
2. Executes a variable-length path Cypher query: `(start)-[:REL_TYPE *1..N]-(reached)`
3. For each reachable node, records the minimum hop distance
4. Groups nodes by hop distance (1-hop, 2-hop, 3-hop, etc.)
5. Counts affected assets by type (users, devices, servers, applications, databases)
6. Identifies critical assets (criticality = "critical" or "high")
7. Collects all relationships used in the traversal paths

**Example request:**

```powershell
Invoke-RestMethod "http://localhost:8000/api/blast-radius/DEV-007?max_hops=3"
```

**Example response (abbreviated):**

```json
{
  "compromised_device": "DEV-007",
  "max_hops": 3,
  "total_affected_assets": 43,
  "hop_1_nodes": [ ... ],
  "hop_2_nodes": [ ... ],
  "hop_3_nodes": [ ... ],
  "affected_counts": {
    "users": 7,
    "devices": 5,
    "servers": 10,
    "applications": 6,
    "databases": 5,
    "ips": 3,
    "vulnerabilities": 3
  },
  "critical_assets": [
    {"id": "DB-001", "labels": ["Database"], "name": "Finance-DB", "criticality": "critical"},
    {"id": "SRV-005", "labels": ["Server"], "name": "db-prod-01", "criticality": "critical"}
  ],
  "relationships": [ ... ],
  "all_nodes": [ ... ]
}
```

---

## Attack Path Discovery

**Endpoint:** `GET /api/attack-path/{source_id}/{target_id}`

Given a source node (e.g. a compromised device) and a target critical asset (e.g. a database), finds the shortest attack paths through the graph.

**Query parameter:**
- `max_paths` (int, default: 5, range: 1–20) — maximum number of paths to return

**Node IDs can be any type:** deviceId, userId, serverId, appId, databaseId, cveId, or IP address.

**How it works:**

1. Resolves both source and target nodes by checking all known ID properties
2. Uses Neo4j's `allShortestPaths` to find all shortest paths
3. For each path, extracts nodes, relationships, and builds a human-readable explanation
4. Returns paths sorted by hop count (shortest first)

**Example request:**

```powershell
Invoke-RestMethod "http://localhost:8000/api/attack-path/DEV-007/DB-001"
```

**Example response:**

```json
{
  "source": {
    "labels": ["Device"],
    "deviceId": "DEV-007",
    "hostname": "Laptop-07",
    "status": "compromised"
  },
  "target": {
    "labels": ["Database"],
    "databaseId": "DB-001",
    "name": "Finance-DB",
    "criticality": "critical"
  },
  "paths_found": 1,
  "shortest_path": {
    "hop_count": 2,
    "nodes": [ ... ],
    "relationships": [ ... ],
    "explanation": "Laptop-07 (Device) →[CONNECTED_TO]→ app-prod-01 (Server) →[ACCESSES]→ Finance-DB (Database)"
  },
  "all_paths": [ ... ]
}
```

**Another example — user to database:**

```powershell
Invoke-RestMethod "http://localhost:8000/api/attack-path/USR-001/DB-001"
```

```
Ateeq Khan (User) →[PRIVILEGED_ACCESS]→ app-prod-01 (Server) →[ACCESSES]→ Finance-DB (Database)
```

---

## Running Phase 2 Tests

With the backend running:

```powershell
cd graphops\backend
python scripts/test_phase2.py
```

This verifies:
- Existing health endpoints still work
- Blast radius returns correct results for valid/invalid devices
- Blast radius respects custom hop limits
- Attack paths are discovered between connected nodes
- 404 errors for non-existent nodes
- Graceful handling of no-path-found cases

---

## Phases

| Phase | Focus                                              | Status       |
|-------|----------------------------------------------------|--------------|
| 1     | Foundation — FastAPI, Neo4j, seed data, health     | ✅ Complete   |
| 2     | Blast-radius API, attack-path discovery            | ✅ Complete   |
| 3     | Interactive graph visualization (Cytoscape)        | ✅ Complete   |
| 4     | ML/GNN-based risk scoring and anomaly detection    | 🔜 Next      |
| 5     | AI-powered containment recommendations             | Planned      |
| 6     | Real-time event streaming (Kafka) and alerting     | Planned      |
| 7     | Containerization, CI/CD, production deployment     | Planned      |

---

## License

Internal / Hackathon project.
