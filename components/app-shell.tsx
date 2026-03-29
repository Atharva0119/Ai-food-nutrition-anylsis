"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

const navItems = [
  { href: "/", label: "Home" },
  { href: "/profile", label: "Profile" },
  { href: "/analysis", label: "Meal Analysis" },
  { href: "/dashboard", label: "Dashboard" },
  { href: "/custom-foods", label: "Custom Foods" }
];

export function AppShell({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="sidebar-brand">
          <span className="sidebar-mark">AI Nutrition</span>
          <h2>Fuel smarter every day.</h2>
          <p>Smart nutrition planner with meal scoring, personalized targets, and simple food tracking.</p>
        </div>

        <nav className="sidebar-nav">
          {navItems.map((item) => {
            const active = pathname === item.href;
            return (
              <Link key={item.href} href={item.href} className={active ? "nav-link active" : "nav-link"}>
                {item.label}
              </Link>
            );
          })}
        </nav>

        <div className="sidebar-tip">
          <strong>Workflow</strong>
          <p>Update your profile, analyze meals, then watch your dashboard totals build up.</p>
        </div>
      </aside>

      <main className="content">{children}</main>
    </div>
  );
}
