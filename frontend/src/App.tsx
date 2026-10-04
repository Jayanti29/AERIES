import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AppShell } from './components/common/AppShell';
import { CommandCenter } from './pages/CommandCenter';
import { CraftDashboard } from './pages/CraftDashboard';
import { PlansPage } from './pages/PlansPage';
import { PilotPages } from './pages/PilotPages';
import { AuditLogPage } from './pages/AuditLogPage';

export const App: React.FC = () => {
  return (
    <BrowserRouter>
      <AppShell>
        <Routes>
          <Route path="/" element={<CommandCenter />} />
          <Route path="/craft" element={<CraftDashboard />} />
          <Route path="/plans" element={<PlansPage />} />
          <Route path="/pilot" element={<PilotPages />} />
          <Route path="/audit" element={<AuditLogPage />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </AppShell>
    </BrowserRouter>
  );
};
