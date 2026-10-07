/**
 * GraphOps API Service.
 *
 * Provides typed functions for all backend endpoints.
 * Phase 1: Health checks.
 * Phase 2: Blast radius & attack path.
 */

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

// ── Health ─────────────────────────────────────────────────

export interface HealthResponse {
  status: string
  service: string
}

export interface Neo4jHealthResponse {
  service: string
  status: string
  message: string
  uri?: string
  database?: string
}

export async function checkApiHealth(): Promise<HealthResponse> {
  const res = await fetch(`${API_URL}/api/health`)
  if (!res.ok) throw new Error(`HTTP ${res.status}`)
  return res.json()
}

export async function checkNeo4jHealth(): Promise<Neo4jHealthResponse> {
  const res = await fetch(`${API_URL}/api/health/neo4j`)
  if (!res.ok) throw new Error(`HTTP ${res.status}`)
  return res.json()
}

// ── Blast Radius ───────────────────────────────────────────

export interface BlastRadiusNode {
  elementId: string
  labels: string[]
  [key: string]: unknown
}

export interface BlastRadiusRel {
  elementId: string
  type: string
  startNodeElementId: string
  endNodeElementId: string
  [key: string]: unknown
}

export interface CriticalAsset {
  id: string
  labels: string[]
  name: string
  criticality: string
}

export interface BlastRadiusResponse {
  compromised_device: string
  max_hops: number
  hop_1_nodes: BlastRadiusNode[]
  hop_2_nodes: BlastRadiusNode[]
  hop_3_nodes: BlastRadiusNode[]
  nodes_by_hop: Record<string, BlastRadiusNode[]>
  total_affected_assets: number
  affected_counts: {
    users: number
    devices: number
    servers: number
    applications: number
    databases: number
    ips: number
    vulnerabilities: number
  }
  critical_assets: CriticalAsset[]
  relationships: BlastRadiusRel[]
  all_nodes: BlastRadiusNode[]
}

export async function getBlastRadius(
  deviceId: string,
  maxHops: number = 3
): Promise<BlastRadiusResponse> {
  const res = await fetch(
    `${API_URL}/api/blast-radius/${encodeURIComponent(deviceId)}?max_hops=${maxHops}`
  )
  if (!res.ok) {
    const body = await res.json().catch(() => ({}))
    throw new Error(body.detail || `HTTP ${res.status}`)
  }
  return res.json()
}

// ── Attack Path ────────────────────────────────────────────

export interface AttackPathNode {
  elementId: string
  labels: string[]
  [key: string]: unknown
}

export interface AttackPathRel {
  elementId: string
  type: string
  startNodeElementId: string
  endNodeElementId: string
  [key: string]: unknown
}

export interface PathData {
  hop_count: number
  nodes: AttackPathNode[]
  relationships: AttackPathRel[]
  explanation: string
}

export interface AttackPathResponse {
  source: AttackPathNode
  target: AttackPathNode
  paths_found: number
  shortest_path?: PathData
  all_paths?: PathData[]
  message?: string
}

export async function getAttackPath(
  sourceId: string,
  targetId: string,
  maxPaths: number = 5
): Promise<AttackPathResponse> {
  const res = await fetch(
    `${API_URL}/api/attack-path/${encodeURIComponent(sourceId)}/${encodeURIComponent(targetId)}?max_paths=${maxPaths}`
  )
  if (!res.ok) {
    const body = await res.json().catch(() => ({}))
    throw new Error(body.detail || `HTTP ${res.status}`)
  }
  return res.json()
}
