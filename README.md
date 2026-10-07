# GraphOps

**Cybersecurity Graph Intelligence Platform**

GraphOps is a threat-hunting and blast-radius analysis platform built around a Neo4j security knowledge graph. It helps security analysts understand the connected environment when a device is compromised — discovering attack paths, mapping blast radius, identifying choke-point nodes, and recommending containment actions.

> **Current status: Phase 1 — Foundation**

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
│   │   ├── main.py            # FastAPI app
│   │   ├── config.py          # Settings from env vars
│   │   ├── database.py        # Neo4j connection service
│   │   ├── routes/health.py   # Health-check endpoints
│   │   └── services/          # Business logic (future phases)
│   ├── scripts/
│   │   ├── seed_database.py   # Populate Neo4j with demo data
│   │   └── clear_database.py  # Clear demo data
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── App.tsx            # Status dashboard
│   │   ├── main.tsx           # React entry point
│   │   ├── index.css          # Styles
│   │   └── services/api.ts   # API client
│   ├── package.json
│   └── .env.example
├── data/                      # Data exports (gitignored)
├── docs/architecture.md       # Architecture docs
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

## API Health Checks

Once the backend is running:

| Endpoint            | Description                  |
|---------------------|------------------------------|
| `GET /api/health`      | API liveness check        |
| `GET /api/health/neo4j` | Neo4j connectivity test  |

Example:

```powershell
Invoke-RestMethod http://localhost:8000/api/health
```

```json
{
  "status": "ok",
  "service": "GraphOps API"
}
```

```powershell
Invoke-RestMethod http://localhost:8000/api/health/neo4j
```

```json
{
  "service": "Neo4j",
  "status": "connected",
  "message": "Neo4j is reachable",
  "uri": "neo4j+s://...",
  "database": "neo4j"
}
```

---

## Phase 1 Limitations

Phase 1 is the **foundation only**. The following are **not** implemented yet:

- Attack-path traversal algorithms
- Blast-radius computation
- Graph visualization / interactive dashboard
- ML/GNN-based risk scoring
- AI-powered explanations or recommendations
- Authentication / authorization
- Real-time event streaming (Kafka)
- Containerization (Docker/Kubernetes)

---

## Future Phases

| Phase | Focus                                              |
|-------|----------------------------------------------------|
| 2     | Blast-radius API, graph traversal, attack-path discovery |
| 3     | Interactive graph visualization (D3.js / Cytoscape) |
| 4     | ML/GNN-based risk scoring and anomaly detection     |
| 5     | AI-powered containment recommendations              |
| 6     | Real-time event streaming (Kafka) and alerting       |
| 7     | Containerization, CI/CD, production deployment       |

---

## License

Internal / Hackathon project.
