

export default function ContainmentPanel() {
  return (
    <div className="panel-section fade-in">
      <div className="panel-section__header">
        <span className="panel-section__icon">🛡️</span>
        <h3 className="panel-section__title">Recommended Containment</h3>
      </div>
      
      <div className="containment-list">
        <div className="containment-item">
          <span className="containment-item__num">1</span>
          <span>Isolate <strong>Laptop-07</strong> from network</span>
        </div>
        <div className="containment-item">
          <span className="containment-item__num">2</span>
          <span>Revoke suspicious privileged session for <strong>Ateeq Khan</strong></span>
        </div>
        <div className="containment-item">
          <span className="containment-item__num">3</span>
          <span>Block suspicious connection to <strong>app-prod-01</strong></span>
        </div>
      </div>
      
      <div className="containment-sim-note">
        SIMULATION — No real security action is performed.
      </div>
    </div>
  );
}
