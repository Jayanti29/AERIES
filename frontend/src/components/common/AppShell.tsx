import React from 'react';
import { HandlingBanner } from './HandlingBanner';
import { Sidebar } from './Sidebar';
import { TopBar } from './TopBar';
import { IdleTimer } from './IdleTimer';

interface AppShellProps {
  children: React.ReactNode;
}

export const AppShell: React.FC<AppShellProps> = ({ children }) => {
  return (
    <div className="min-h-screen bg-[#0B1220] text-[#E8EDF7] flex flex-col font-sans">
      <HandlingBanner />
      <IdleTimer />
      <div className="flex flex-1 overflow-hidden">
        <Sidebar />
        <div className="flex-1 flex flex-col overflow-y-auto">
          <TopBar />
          <main className="flex-1 p-6 space-y-6">
            {children}
          </main>
          <footer className="h-8 bg-[#0B1220] border-t border-[#24304A] px-6 flex items-center justify-between text-[11px] font-mono text-[#7A869C]">
            <div>UTC CLOCK: 2026-10-05 11:24:00Z</div>
            <div>AERIS CORE ENGINE v1.4.2 // POSTGRES POSTGIS 15 // REDIS 7 // CP-SAT</div>
            <div className="text-[#D99A1B]">RESTRICTED SIMULATION</div>
          </footer>
        </div>
      </div>
    </div>
  );
};
