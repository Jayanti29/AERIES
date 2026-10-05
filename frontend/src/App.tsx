import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AppShell } from './components/common/AppShell';
import { CommandCenter } from './pages/CommandCenter';
import { OperationalMapPage } from './pages/OperationalMapPage';
import { InsightsPage } from './pages/InsightsPage';
import { CraftDashboard } from './pages/CraftDashboard';
import { SupplyDashboard } from './pages/SupplyDashboard';
import { PeopleDashboard } from './pages/PeopleDashboard';
import { PilotPages } from './pages/PilotPages';
import { PlansPage } from './pages/PlansPage';
import { TradeoffExplorer } from './pages/TradeoffExplorer';
import { DependencyGraphPage } from './pages/DependencyGraphPage';
import { ChaosLabPage } from './pages/ChaosLabPage';
import { StressTestPage } from './pages/StressTestPage';
import { DecisionQueuePage } from './pages/DecisionQueuePage';
import { DecisionHistoryPage } from './pages/DecisionHistoryPage';
import { DataHealthPage } from './pages/DataHealthPage';
import { ModelRegistryPage } from './pages/ModelRegistryPage';
import { AuditLogPage } from './pages/AuditLogPage';
import { AdminPage } from './pages/AdminPage';
import { AccountPage } from './pages/AccountPage';

export const App: React.FC = () => {
  return (
    <BrowserRouter>
      <AppShell>
        <Routes>
          <Route path="/" element={<CommandCenter />} />
          <Route path="/map" element={<OperationalMapPage />} />
          <Route path="/insights" element={<InsightsPage />} />
          <Route path="/craft" element={<CraftDashboard />} />
          <Route path="/supply" element={<SupplyDashboard />} />
          <Route path="/people" element={<PeopleDashboard />} />
          <Route path="/pilot" element={<PilotPages />} />
          <Route path="/plans" element={<PlansPage />} />
          <Route path="/tradeoffs" element={<TradeoffExplorer />} />
          <Route path="/graph" element={<DependencyGraphPage />} />
          <Route path="/chaos" element={<ChaosLabPage />} />
          <Route path="/stress" element={<StressTestPage />} />
          <Route path="/decisions" element={<DecisionQueuePage />} />
          <Route path="/replay" element={<DecisionHistoryPage />} />
          <Route path="/data-health" element={<DataHealthPage />} />
          <Route path="/models" element={<ModelRegistryPage />} />
          <Route path="/audit" element={<AuditLogPage />} />
          <Route path="/admin" element={<AdminPage />} />
          <Route path="/account" element={<AccountPage />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </AppShell>
    </BrowserRouter>
  );
};
