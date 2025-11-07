// src/views/CountdownTimer.tsx
import { useState, useEffect } from "react";

export default function CountdownTimer() {
  const [seconds, setSeconds] = useState<number>(10);
  const [isRunning, setIsRunning] = useState<boolean>(false);

  useEffect(() => {
    let timer: NodeJS.Timeout | null = null;
    if (isRunning && seconds > 0) {
      timer = setInterval(() => {
        setSeconds((prev) => prev - 1);
      }, 1000);
    }
    if (seconds === 0) {
      setIsRunning(false);
    }
    return () => {
      if (timer) clearInterval(timer);
    };
  }, [isRunning, seconds]);

  const handleStart = () => {
    if (seconds > 0) setIsRunning(true);
  };

  const handleReset = () => {
    setIsRunning(false);
    setSeconds(10);
  };

  return (
    <div className="flex items-center justify-center h-screen bg-gradient-to-br from-emerald-100 via-mint-200 to-pink-100">
      <div className="rounded-3xl shadow-lg p-10 text-center bg-white/70 backdrop-blur-md border border-emerald-200">
        <h1 className="text-3xl font-bold text-emerald-600 mb-6">
          ⏳ Contador Regresivo
        </h1>
        <label
          htmlFor="seconds"
          className="block mb-4 text-lg font-medium text-slate-700"
        >
          Segundos:
        </label>
        <input
          id="seconds"
          aria-label="Segundos"
          type="number"
          value={seconds}
          onChange={(e) => setSeconds(Number(e.target.value))}
          className="px-4 py-2 border rounded-lg text-center mb-6"
        />
        <div className="text-4xl font-mono font-bold text-rose-500 mb-6">
          {seconds > 0 ? `${seconds} segundos restantes` : "¡Tiempo terminado!"}
        </div>
        <div className="flex justify-center gap-4">
          <button
            onClick={handleStart}
            disabled={isRunning || seconds === 0}
            className="px-4 py-2 rounded-lg bg-emerald-500 text-white font-semibold hover:bg-emerald-600 disabled:opacity-50"
          >
            🚀 Iniciar
          </button>
          <button
            onClick={handleReset}
            className="px-4 py-2 rounded-lg bg-rose-500 text-white font-semibold hover:bg-rose-600"
          >
            Reiniciar
          </button>
        </div>
      </div>
    </div>
  );
}
