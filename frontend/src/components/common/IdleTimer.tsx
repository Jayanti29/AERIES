import React, { useState, useEffect } from 'react';
import { Clock, ShieldAlert } from 'lucide-react';
import { useAuthStore } from '../../store/authStore';

export const IdleTimer: React.FC = () => {
  const [secondsRemaining, setSecondsRemaining] = useState(15 * 60);
  const [showWarning, setShowWarning] = useState(false);
  const { clearAuth } = useAuthStore();

  useEffect(() => {
    const handleActivity = () => {
      if (!showWarning) {
        setSecondsRemaining(15 * 60);
      }
    };

    window.addEventListener('mousemove', handleActivity);
    window.addEventListener('keydown', handleActivity);

    const interval = setInterval(() => {
      setSecondsRemaining((prev) => {
        if (prev <= 1) {
          clearInterval(interval);
          clearAuth();
          return 0;
        }
        if (prev <= 60 && !showWarning) {
          setShowWarning(true);
        }
        return prev - 1;
      });
    }, 1000);

    return () => {
      window.removeEventListener('mousemove', handleActivity);
      window.removeEventListener('keydown', handleActivity);
      clearInterval(interval);
    };
  }, [showWarning, clearAuth]);

  if (!showWarning || secondsRemaining === 0) return null;

  const extendSession = () => {
    setSecondsRemaining(15 * 60);
    setShowWarning(false);
  };

  return (
    <div className="fixed inset-0 bg-black/80 backdrop-blur-sm flex items-center justify-center z-50 p-4 font-mono select-none">
      <div className="bg-[#111A2E] border border-[#E5484D] w-full max-w-sm rounded-lg p-5 shadow-2xl text-center space-y-4">
        <div className="w-12 h-12 rounded-full bg-[#2D161A] border border-[#E5484D]/40 mx-auto flex items-center justify-center text-[#E5484D]">
          <Clock className="w-6 h-6 animate-pulse" />
        </div>
        <div>
          <h3 className="text-sm font-bold text-[#E8EDF7] uppercase tracking-wide">Inactivity Logout Warning</h3>
          <p className="text-xs text-[#9AA7BF] mt-1">Per Security Rule SEC-05: Session will terminate in</p>
          <div className="text-3xl font-bold font-mono text-[#E5484D] mt-2">{secondsRemaining}s</div>
        </div>
        <div className="flex space-x-3 pt-2">
          <button
            onClick={() => clearAuth()}
            className="flex-1 py-1.5 border border-[#24304A] text-xs text-[#9AA7BF] hover:bg-[#172238] rounded"
          >
            Sign Out Now
          </button>
          <button
            onClick={extendSession}
            className="flex-1 py-1.5 bg-[#3B82F6] hover:bg-blue-600 text-white text-xs font-bold rounded"
          >
            Extend Session
          </button>
        </div>
      </div>
    </div>
  );
};
