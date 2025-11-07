// src/views/CountdownTimer.tsx
import { useEffect, useRef, useState } from "react";

/**
 * CountdownTimer robusto:
 * - input como string para permitir campo vacío
 * - parseInt seguro al iniciar
 * - timerRef con window.setInterval (número) y limpieza correcta
 * - botones type="button" (no submit)
 */
export default function CountdownTimer() {
  const [inputValue, setInputValue] = useState<string>("60"); // valor mostrado en input
  const [timeLeft, setTimeLeft] = useState<number>(0);
  const [running, setRunning] = useState<boolean>(false);

  // en navegador window.setInterval devuelve un number
  const timerRef = useRef<number | null>(null);

  // efecto para el intervalo; se crea sólo cuando running === true
  useEffect(() => {
    if (!running) return;

    // evita multiples intervalos
    if (timerRef.current !== null) {
      clearInterval(timerRef.current);
      timerRef.current = null;
    }

    timerRef.current = window.setInterval(() => {
      setTimeLeft((prev) => {
        if (prev <= 1) {
          // si llega a 0 o menor, limpiamos y detenemos
          if (timerRef.current !== null) {
            clearInterval(timerRef.current);
            timerRef.current = null;
          }
          setRunning(false);
          return 0;
        }
        return prev - 1;
      });
    }, 1000);

    // cleanup si el componente se desmonta o running cambia
    return () => {
      if (timerRef.current !== null) {
        clearInterval(timerRef.current);
        timerRef.current = null;
      }
    };
  }, [running]);

  // manejar inicio
  const handleStart = () => {
    // parsear el input de forma segura
    const parsed = parseInt(inputValue, 10);
    if (isNaN(parsed) || parsed <= 0) {
      // opcional: indicar al usuario que el valor no es válido
      setTimeLeft(0);
      setRunning(false);
      return;
    }
    setTimeLeft(parsed);
    setRunning(true);
  };

  // reiniciar
  const handleReset = () => {
    if (timerRef.current !== null) {
      clearInterval(timerRef.current);
      timerRef.current = null;
    }
    setRunning(false);
    setTimeLeft(0);
    setInputValue(""); // limpia el campo (opcional)
  };

  return (
    <div className="flex items-center justify-center h-full p-6">
      <div className="w-full max-w-md bg-white dark:bg-slate-800 rounded-2xl shadow-lg p-6 text-center">
        <h1 className="text-2xl font-bold text-slate-800 dark:text-slate-100 mb-6">
          ⏳ Contador Regresivo
        </h1>

        {/* Input (string) para evitar NaN cuando está vacío */}
        <input
          type="number"
          min={1}
          placeholder="Ingresa segundos"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          className="w-full px-4 py-2 mb-4 border border-slate-300 dark:border-slate-600 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:outline-none"
          aria-label="Segundos"
          disabled={running} // evita cambiar mientras corre (opcional)
        />

        {/* Botones con type="button" -> no envían formularios */}
        <div className="flex gap-3">
          <button
            type="button"
            onClick={handleStart}
            className="flex-1 bg-emerald-500 hover:bg-emerald-600 text-white font-semibold text-lg py-3 rounded-xl shadow-md transition-transform transform hover:scale-105 disabled:bg-gray-400"
            disabled={running || inputValue.trim() === "" || (parseInt(inputValue, 10) || 0) <= 0}
          >
            {running ? "En marcha..." : "🚀 Iniciar"}
          </button>

          <button
            type="button"
            onClick={handleReset}
            className="flex-1 bg-red-500 hover:bg-red-600 text-white font-semibold text-lg py-3 rounded-xl shadow-md transition-transform transform hover:scale-105"
          >
            🔄 Reiniciar
          </button>
        </div>

        {/* Visualización del tiempo */}
        <div className="mt-6 text-5xl font-bold text-emerald-600">
          {timeLeft > 0 ? timeLeft : "¡Tiempo terminado!"}
        </div>
      </div>
    </div>
  );
}
