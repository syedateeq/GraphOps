const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

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
