import type { BlastRadiusResponse } from '../../services/api';

interface BlastRadiusPanelProps {
  data: BlastRadiusResponse;
}

export default function BlastRadiusPanel({ data }: BlastRadiusPanelProps) {
  return (
    <div className="panel-section fade-in">
      <div className="panel-section__header">
        <span className="panel-section__icon">💥</span>
        <h3 className="panel-section__title">Blast Radius Analysis</h3>
      </div>
      
      <div className="blast-stats" style={{ marginBottom: '1rem' }}>
        <div className="blast-stat">
          <div className="blast-stat__num">{data.total_affected_assets}</div>
          <div className="blast-stat__label">Total Assets</div>
        </div>
        <div className="blast-stat">
          <div className="blast-stat__num" style={{ color: 'var(--red)' }}>{data.critical_assets.length}</div>
          <div className="blast-stat__label">Critical</div>
        </div>
        <div className="blast-stat">
          <div className="blast-stat__num">{data.max_hops}</div>
          <div className="blast-stat__label">Max Hops</div>
        </div>
      </div>

      <div className="detail-grid">
        <div className="detail-item">
          <span className="detail-item__label">Users</span>
          <span className="detail-item__value">{data.affected_counts.users}</span>
        </div>
        <div className="detail-item">
          <span className="detail-item__label">Servers</span>
          <span className="detail-item__value">{data.affected_counts.servers}</span>
        </div>
        <div className="detail-item">
          <span className="detail-item__label">Databases</span>
          <span className="detail-item__value">{data.affected_counts.databases}</span>
        </div>
        <div className="detail-item">
          <span className="detail-item__label">Apps</span>
          <span className="detail-item__value">{data.affected_counts.applications}</span>
        </div>
      </div>
    </div>
  );
}
