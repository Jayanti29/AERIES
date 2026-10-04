import { create } from 'zustand';
import { User, Role } from '../types';

interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  theme: 'dark' | 'light';
  setAuth: (user: User, token: string) => void;
  clearAuth: () => void;
  toggleTheme: () => void;
  switchRole: (role: Role) => void;
}

export const useAuthStore = create<AuthState>((set) => ({
  user: {
    id: 'usr-planner',
    username: 'planner',
    role: 'Operations Planner',
    callsign: 'STRATEGIST'
  },
  token: 'mock-initial-token',
  isAuthenticated: true,
  theme: 'dark',
  setAuth: (user, token) => set({ user, token, isAuthenticated: true }),
  clearAuth: () => set({ user: null, token: null, isAuthenticated: false }),
  toggleTheme: () => set((state) => ({ theme: state.theme === 'dark' ? 'light' : 'dark' })),
  switchRole: (role: Role) => set((state) => ({
    user: state.user ? { ...state.user, role, username: role.toLowerCase().replace(/\s+/g, '_') } : null
  }))
}));
