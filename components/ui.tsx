import type { ReactNode } from "react";

export function Hero({
  title,
  subtitle,
  pills
}: {
  title: string;
  subtitle: string;
  pills?: string[];
}) {
  return (
    <section className="hero">
      <div className="hero-kicker">Nutrition Intelligence</div>
      <h1>{title}</h1>
      <p>{subtitle}</p>
      {pills ? (
        <div className="pill-row">
          {pills.map((pill) => (
            <span className="pill" key={pill}>
              {pill}
            </span>
          ))}
        </div>
      ) : null}
    </section>
  );
}

export function Card({
  title,
  children,
  actions
}: {
  title?: string;
  children: ReactNode;
  actions?: ReactNode;
}) {
  return (
    <section className="card">
      {title ? <h2 className="card-title">{title}</h2> : null}
      {actions ? <div className="card-actions">{actions}</div> : null}
      {children}
    </section>
  );
}

export function StatGrid({
  items
}: {
  items: { label: string; value: string | number; help?: string }[];
}) {
  return (
    <div className="stat-grid">
      {items.map((item) => (
        <div className="stat-card" key={item.label}>
          <div className="stat-label">{item.label}</div>
          <div className="stat-value">{item.value}</div>
          {item.help ? <div className="stat-help">{item.help}</div> : null}
        </div>
      ))}
    </div>
  );
}

export function ProgressBar({ value }: { value: number }) {
  return (
    <div className="progress-shell" aria-label="Progress">
      <div className="progress-fill" style={{ width: `${Math.max(0, Math.min(100, value))}%` }} />
    </div>
  );
}

export function Badge({ children }: { children: ReactNode }) {
  return <span className="badge">{children}</span>;
}
