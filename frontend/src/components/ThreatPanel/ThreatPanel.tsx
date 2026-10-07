

interface ThreatPanelProps {
  onAnalyzeBlastRadius: () => void;
  isAnalyzing: boolean;
  hasAnalyzed: boolean;
}

export default function ThreatPanel({ onAnalyzeBlastRadius, isAnalyzing, hasAnalyzed }: ThreatPanelProps) {
  return (
    <div className="panel-section">
      <div className="panel-section__header">
        <span className="panel-section__icon">🚨</span>
        <h3 className="panel-section__title">Security Incident</h3>
        <span className="panel-section__badge panel-section__badge--red">CRITICAL</span>
      </div>
      
      <div className="detail-grid" style={{ marginBottom: '1rem' }}>
        <div className="detail-item">
          <span className="detail-item__label">Device</span>
          <span className="detail-item__value">Laptop-07 (DEV-007)</span>
        </div>
        <div className="detail-item">
          <span className="detail-item__label">Status</span>
          <span className="detail-item__value detail-item__value--red">COMPROMISED</span>
        </div>
        <div className="detail-item">
          <span className="detail-item__label">Risk Score</span>
          <span className="detail-item__value detail-item__value--red">92 / 100</span>
        </div>
      </div>

      <button 
        className="btn btn--primary" 
        onClick={onAnalyzeBlastRadius}
        disabled={isAnalyzing || hasAnalyzed}
      >
        {isAnalyzing ? (
          <>
            <span className="loading-spinner" style={{ width: '12px', height: '12px' }}></span>
            Analyzing...
          </>
        ) : hasAnalyzed ? (
          'Blast Radius Analyzed'
        ) : (
          'Analyze Blast Radius'
        )}
      </button>
    </div>
  );
}
