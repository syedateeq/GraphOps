import { useState, useEffect } from 'react'
import { checkApiHealth, checkNeo4jHealth } from './services/api'

type ConnectionStatus = 'checking' | 'connected' | 'disconnected'

function App() {
  const [apiStatus, setApiStatus] = useState<ConnectionStatus>('checking')
  const [neo4jStatus, setNeo4jStatus] = useState<ConnectionStatus>('checking')

  useEffect(() => {
    // Check API health
    checkApiHealth()
      .then((data) => {
        setApiStatus(data.status === 'ok' ? 'connected' : 'disconnected')
      })
      .catch(() => {
        setApiStatus('disconnected')
      })

    // Check Neo4j health
    checkNeo4jHealth()
      .then((data) => {
        setNeo4jStatus(data.status === 'connected' ? 'connected' : 'disconnected')
      })
      .catch(() => {
        setNeo4jStatus('disconnected')
      })
  }, [])

  const statusLabel = (s: ConnectionStatus) => {
    if (s === 'checking') return 'CHECKING…'
    if (s === 'connected') return 'CONNECTED'
    return 'DISCONNECTED'
  }

  return (
    <div className="app-container">
      {/* Header */}
      <header className="header">
        <h1 className="header__logo">GraphOps</h1>
        <p className="header__tagline">
          Cybersecurity Graph Intelligence Platform
        </p>
        <span className="header__phase">Phase 1 — Foundation</span>
      </header>

      {/* Status Cards */}
      <section className="status-grid">
        <div className="status-card">
          <div className="status-card__label">Backend API</div>
          <div className="status-card__indicator">
            <span className={`status-dot status-dot--${apiStatus}`} />
            <span className={`status-card__text status-card__text--${apiStatus}`}>
              {statusLabel(apiStatus)}
            </span>
          </div>
        </div>

        <div className="status-card">
          <div className="status-card__label">Neo4j Database</div>
          <div className="status-card__indicator">
            <span className={`status-dot status-dot--${neo4jStatus}`} />
            <span className={`status-card__text status-card__text--${neo4jStatus}`}>
              {statusLabel(neo4jStatus)}
            </span>
          </div>
        </div>
      </section>

      {/* Project Info */}
      <section className="info-section">
        <h2 className="info-section__title">Project Information</h2>
        <table className="info-table">
          <tbody>
            <tr>
              <td>Project</td>
              <td>GraphOps</td>
            </tr>
            <tr>
              <td>Version</td>
              <td>0.1.0</td>
            </tr>
            <tr>
              <td>Phase</td>
              <td>1 — Foundation</td>
            </tr>
            <tr>
              <td>Backend</td>
              <td>FastAPI + Uvicorn</td>
            </tr>
            <tr>
              <td>Frontend</td>
              <td>React + Vite</td>
            </tr>
            <tr>
              <td>Database</td>
              <td>Neo4j (AuraDB compatible)</td>
            </tr>
            <tr>
              <td>Graph Nodes</td>
              <td>User · Device · IP · Server · App · Database · Vulnerability</td>
            </tr>
            <tr>
              <td>Description</td>
              <td>Threat-hunting and blast-radius analysis via security knowledge graph</td>
            </tr>
          </tbody>
        </table>
      </section>
    </div>
  )
}

export default App
