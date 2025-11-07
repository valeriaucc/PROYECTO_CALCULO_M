// src/views/DigitalClock.tsx
import { useEffect, useState } from "react";

export default function DigitalClock() {
  const [time, setTime] = useState<string>("");

  useEffect(() => {
    const updateClock = () => {
      const now = new Date();
      const hh = String(now.getHours()).padStart(2, "0");
      const mm = String(now.getMinutes()).padStart(2, "0");
      const ss = String(now.getSeconds()).padStart(2, "0");
      setTime(`${hh}:${mm}:${ss}`);
    };

    updateClock();
    const timer = setInterval(updateClock, 1000);
    return () => clearInterval(timer);
  }, []);

  return (
    <div className="flex items-center justify-center h-screen bg-gradient-to-br from-pink-200 via-rose-100 to-mint-200">
      <div className="rounded-3xl shadow-xl p-10 text-center bg-white/60 backdrop-blur-lg border border-pink-100">
        <h1 className="text-3xl font-extrabold text-rose-500 mb-8 drop-shadow-sm">
          Reloj Digital
        </h1>
        <div
          data-testid="clock-time"
          className="text-7xl font-mono font-bold text-transparent bg-clip-text bg-gradient-to-r from-rose-400 to-emerald-400 animate-pulse"
        >
          {time}
        </div>
        <p className="mt-6 text-emerald-600 text-sm font-medium">
          Hora actual en tu dispositivo ⏰
        </p>
      </div>
    </div>
  );
}
