# GraphOps Architecture

## Overview

GraphOps is a cybersecurity threat-hunting and blast-radius analysis platform built around a **Neo4j security knowledge graph**.

When a security alert says a device is compromised, GraphOps helps analysts understand:
1. What the attacker can potentially reach
2. The attack path to critical assets
3. The blast radius of a compromise
4. High-risk / choke-point nodes in the network
5. Recommended containment actions

## System Architecture (Phase 1)

```
┌──────────────┐        HTTP/REST        ┌──────────────┐        Bolt        ┌──────────────┐
│              │  ──────────────────────► │              │ ──────────────────►│              │
│   React +    │                         │   FastAPI +   │                    │    Neo4j     │
│   Vite       │  ◄────────────────────  │   Uvicorn    │ ◄──────────────────│   (AuraDB)   │
│   Frontend   │        JSON             │   Backend    │       Cypher       │   Database   │
│              │                         │              │                    │              │
└──────────────┘                         └──────────────┘                    └──────────────┘
   Port 5173                                Port 8000                        Port 7687
```

## Neo4j Graph Schema

### Node Types

| Label          | Key Property   | Description                        |
|----------------|----------------|------------------------------------|
| User           | userId         | Employee / account                 |
| Device         | deviceId       | Endpoint (laptop, desktop, etc.)   |
| IP             | address        | Network address                    |
| Server         | serverId       | Infrastructure server              |
| Application    | appId          | Software application               |
| Database       | databaseId     | Data store                         |
| Vulnerability  | cveId          | Known vulnerability (CVE)          |

### Relationships

| Relationship         | From         → To          | Meaning                                |
|----------------------|----------------------------|----------------------------------------|
| USES                 | User         → Device      | User operates the device               |
| HAS_IP               | Device       → IP          | Device has network address             |
| CONNECTED_TO         | Device       → Server      | Device communicates with server        |
| RUNS                 | Server       → Application | Server hosts the application           |
| ACCESSES             | Application  → Database    | Application reads/writes database      |
| ACCESSES             | Server       → Database    | Server directly accesses database      |
| HAS_VULNERABILITY    | Device       → Vulnerability | Device has a known CVE               |
| PRIVILEGED_ACCESS    | User         → Server      | User has admin/elevated access         |
| COMMUNICATES_WITH    | Server       → Server      | Server-to-server communication         |

## Attack Scenario (Embedded in Graph)

The seed data contains a realistic multi-hop attack path:

```
Laptop-07 (compromised, CVE-2024-21351 + CVE-2024-21412 + CVE-2023-44228)
    │
    │ USES (reverse)
    ▼
User: Ateeq Khan (DevOps, privileged)
    │
    │ PRIVILEGED_ACCESS
    ▼
Server: app-prod-01 (Application server, high criticality)
    │
    │ COMMUNICATES_WITH / ACCESSES
    ▼
Server: db-prod-01 (Database server, critical)
    │
    │ ACCESSES
    ▼
Database: Finance-DB (critical)
```

This path is **not hard-coded** as a feature — it exists naturally in the relationships, ready to be discovered by future graph traversal algorithms.

## Directory Structure

```
graphops/
├── backend/
│   ├── app/
│   │   ├── main.py          # FastAPI entry point
│   │   ├── config.py        # Environment configuration
│   │   ├── database.py      # Neo4j connection service
│   │   ├── routes/
│   │   │   └── health.py    # Health check endpoints
│   │   └── services/        # Business logic (Phase 2+)
│   ├── scripts/
│   │   ├── seed_database.py # Populate Neo4j with demo data
│   │   └── clear_database.py# Remove demo data
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── App.tsx          # Main application component
│   │   ├── main.tsx         # React entry point
│   │   ├── index.css        # Styles
│   │   └── services/
│   │       └── api.ts       # Backend API client
│   ├── package.json
│   └── .env.example
├── data/                    # Data exports (not committed)
├── docs/
│   └── architecture.md     # This file
├── .gitignore
└── README.md
```

## Future Phases

| Phase | Focus                                      |
|-------|--------------------------------------------|
| 2     | Blast-radius API, graph traversal, attack-path discovery |
| 3     | Interactive graph visualization dashboard  |
| 4     | ML/GNN-based risk scoring                  |
| 5     | AI-powered containment recommendations     |
| 6     | Real-time event streaming (Kafka)          |
