import type { Metadata } from "next";

import { AppShell } from "@/components/app-shell";
import { AppStateProvider } from "@/lib/app-state";

import "./globals.css";

export const metadata: Metadata = {
  title: "AI Nutrition Assistant",
  description: "A Vercel-ready food nutrition analysis app."
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body>
        <AppStateProvider>
          <AppShell>{children}</AppShell>
        </AppStateProvider>
      </body>
    </html>
  );
}
