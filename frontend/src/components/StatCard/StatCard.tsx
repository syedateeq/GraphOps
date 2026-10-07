

interface StatCardProps {
  label: string;
  value: string | number;
  subValue?: string;
  variant?: 'threat' | 'critical' | 'compromised' | 'risk' | 'default';
}

export default function StatCard({ label, value, subValue, variant = 'default' }: StatCardProps) {
  return (
    <div className={`stat-card stat-card--${variant}`}>
      <div className="stat-card__label">{label}</div>
      <div className="stat-card__value">{value}</div>
      {subValue && <div className="stat-card__sub">{subValue}</div>}
    </div>
  );
}
