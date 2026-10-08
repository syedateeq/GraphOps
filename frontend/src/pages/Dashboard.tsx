import { useState, useEffect } from 'react';
import SecurityGraph from '../components/SecurityGraph/SecurityGraph';
import StatCard from '../components/StatCard/StatCard';
import ThreatPanel from '../components/ThreatPanel/ThreatPanel';
import BlastRadiusPanel from '../components/BlastRadiusPanel/BlastRadiusPanel';
import AttackPathPanel from '../components/AttackPathPanel/AttackPathPanel';
import ContainmentPanel from '../components/ContainmentPanel/ContainmentPanel';
import { checkApiHealth, checkNeo4jHealth, getBlastRadius, getAttackPath, BlastRadiusResponse, AttackPathResponse } from '../services/api';

export default function Dashboard() {
  const [apiOk, setApiOk] = useState(false);
  const [dbOk, setDbOk] = useState(false);
  const [loadingInitial, setLoadingInitial] = useState(true);

  // Analysis state
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [blastRadius, setBlastRadius] = useState<BlastRadiusResponse | null>(null);
  
  // Attack path state
  const [isFindingPath, setIsFindingPath] = useState(false);
  const [attackPath, setAttackPath] = useState<AttackPathResponse | null>(null);

  const [highlightMode, setHighlightMode] = useState<'none' | 'blast' | 'attack'>('none');

  useEffect(() => {
    Promise.all([checkApiHealth().catch(()=>null), checkNeo4jHealth().catch(()=>null)]).then(([api, db]) => {
      setApiOk(api?.status === 'ok');
      setDbOk(db?.status === 'connected');
      setLoadingInitial(false);
    });
  }, []);

  const handleAnalyzeBlastRadius = async () => {
    setIsAnalyzing(true);
    setHighlightMode('none');
    try {
      const result = await getBlastRadius('DEV-007', 3);
      setBlastRadius(result);
      setHighlightMode('blast');
      setAttackPath(null); // clear attack path if showing blast radius
    } catch (err) {
      console.error('Failed to get blast radius:', err);
      alert('Failed to compute blast radius. Ensure backend is running.');
    } finally {
      setIsAnalyzing(false);
    }
  };

  const handleFindAttackPath = async (targetId: string) => {
    setIsFindingPath(true);
    try {
      const result = await getAttackPath('DEV-007', targetId);
      setAttackPath(result);
      setHighlightMode('attack');
    } catch (err) {
      console.error('Failed to get attack path:', err);
      alert('Failed to discover attack path.');
    } finally {
      setIsFindingPath(false);
    }
  };

  if (loadingInitial) {
    return (
      <div className="loading-overlay">
        <span className="loading-spinner"></span>
        <span className="loading-overlay__text">Loading GraphOps...</span>
      </div>
    );
  }

  return (
    <div className="dashboard">
      <header className="dash-header">
        <div className="dash-header__brand">
          <div className="dash-header__logo">GraphOps</div>
          <div className="dash-header__sep"></div>
          <div className="dash-header__tagline">Proactive Threat Hunting & Blast Radius</div>
          <div className="dash-header__phase">Phase 3</div>
        </div>
        <div className="dash-header__right">
          <div className="dash-header__status">
            API <span className={`dash-header__status-dot ${apiOk ? 'dash-header__status-dot--ok' : 'dash-header__status-dot--err'}`}></span>
          </div>
          <div className="dash-header__status">
            Neo4j <span className={`dash-header__status-dot ${dbOk ? 'dash-header__status-dot--ok' : 'dash-header__status-dot--err'}`}></span>
          </div>
        </div>
      </header>

      <div className="stat-row">
        <StatCard label="Active Threats" value="12" variant="threat" />
        <StatCard label="Critical Assets" value="3" variant="critical" />
        <StatCard label="Compromised Devices" value="1" variant="compromised" />
        <StatCard label="High Risk Nodes" value="8" variant="risk" />
      </div>

      <div className="dash-main">
        <div className="graph-area" style={{ position: 'relative' }}>
          <div className="graph-toolbar">
            <div className="graph-toolbar__title">Security Knowledge Graph</div>
            <button className={`graph-toolbar__btn ${highlightMode === 'none' ? 'graph-toolbar__btn--active' : ''}`} onClick={() => setHighlightMode('none')}>Default View</button>
            <button className={`graph-toolbar__btn ${highlightMode === 'blast' ? 'graph-toolbar__btn--active' : ''}`} disabled={!blastRadius} onClick={() => setHighlightMode('blast')}>Show Blast Radius</button>
            <button className={`graph-toolbar__btn ${highlightMode === 'attack' ? 'graph-toolbar__btn--active' : ''}`} disabled={!attackPath} onClick={() => setHighlightMode('attack')}>Show Attack Path</button>
          </div>
          
          <SecurityGraph 
            blastRadius={blastRadius} 
            attackPath={attackPath} 
            highlightMode={highlightMode} 
          />
          
          {(!blastRadius && !attackPath) && (
            <div className="graph-empty" style={{position: 'absolute', top: '40px', left: 0, right: 0, bottom: 0, pointerEvents: 'none'}}>
              <div className="graph-empty__icon">🔍</div>
              <div>Select "Analyze Blast Radius" to load the graph.</div>
            </div>
          )}
        </div>

        <aside className="right-panel">
          <ThreatPanel 
            onAnalyzeBlastRadius={handleAnalyzeBlastRadius} 
            isAnalyzing={isAnalyzing} 
            hasAnalyzed={!!blastRadius} 
          />
          {blastRadius && (
            <BlastRadiusPanel data={blastRadius} />
          )}
          {blastRadius && (
            <AttackPathPanel 
              criticalAssets={blastRadius.critical_assets} 
              onFindPath={handleFindAttackPath} 
              attackPath={attackPath} 
              isFinding={isFindingPath} 
            />
          )}
          {attackPath && (
            <ContainmentPanel />
          )}
        </aside>
      </div>
    </div>
  );
}
