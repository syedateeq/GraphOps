import { useState } from 'react';
import React from 'react';
import type { AttackPathResponse, CriticalAsset, AttackPathNode } from '../../services/api';

interface AttackPathPanelProps {
  criticalAssets: CriticalAsset[];
  onFindPath: (targetId: string) => void;
  attackPath: AttackPathResponse | null;
  isFinding: boolean;
}

export default function AttackPathPanel({ criticalAssets, onFindPath, attackPath, isFinding }: AttackPathPanelProps) {
  const [selectedTarget, setSelectedTarget] = useState<string>('DB-001');

  const handleFindPath = () => {
    onFindPath(selectedTarget);
  };

  return (
    <div className="panel-section fade-in">
      <div className="panel-section__header">
        <span className="panel-section__icon">⚡</span>
        <h3 className="panel-section__title">Attack Path Discovery</h3>
      </div>
      
      <div className="target-selector" style={{ marginBottom: '1rem' }}>
        <div className="target-selector__row">
          <span className="target-selector__label">Source</span>
          <select className="threat-select" disabled>
            <option>DEV-007 (Laptop-07)</option>
          </select>
        </div>
        <div className="target-selector__row">
          <span className="target-selector__label">Target</span>
          <select 
            className="threat-select" 
            value={selectedTarget}
            onChange={(e) => setSelectedTarget(e.target.value)}
          >
            {criticalAssets.map(asset => (
              <option key={asset.id} value={asset.id}>
                {asset.name} ({asset.id})
              </option>
            ))}
            {criticalAssets.length === 0 && <option value="DB-001">Finance-DB (DB-001)</option>}
          </select>
        </div>
      </div>

      <button 
        className="btn btn--ghost" 
        onClick={handleFindPath}
        disabled={isFinding}
        style={{ marginBottom: '1rem' }}
      >
        {isFinding ? 'Discovering...' : 'Find Attack Path'}
      </button>

      {attackPath && attackPath.shortest_path && (
        <div className="attack-path-visual fade-in">
          {attackPath.shortest_path.nodes.map((node: AttackPathNode, i: number) => {
            const rel = attackPath.shortest_path!.relationships[i];
            const nodeName = node.name || node.hostname || node.deviceId || node.databaseId || node.elementId;
            const isSource = i === 0;
            const isTarget = i === attackPath.shortest_path!.nodes.length - 1;
            
            return (
              <React.Fragment key={i}>
                <div className={`attack-path-node ${isSource ? 'attack-path-node--source' : isTarget ? 'attack-path-node--target' : ''}`}>
                  <span className="attack-path-node__dot" style={{ background: isSource ? 'var(--red)' : isTarget ? 'var(--orange)' : 'var(--accent)' }}></span>
                  <span>{nodeName as string}</span>
                  <span className="attack-path-node__label">{node.labels[0]}</span>
                </div>
                {rel && (
                  <div className="attack-path-edge">
                    <span className="attack-path-edge__arrow">↓</span>
                    <span className="attack-path-edge__label">{rel.type}</span>
                  </div>
                )}
              </React.Fragment>
            );
          })}
        </div>
      )}
      
      {attackPath && attackPath.paths_found === 0 && (
        <div className="info-banner fade-in">
          No attack paths found to target.
        </div>
      )}
    </div>
  );
}
