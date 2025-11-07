// src/views/ColorPicker.tsx
import { useEffect, useState } from "react";

export default function ColorPicker() {
  const [color, setColor] = useState<string>(() => {
    // Recuperar color guardado o usar blanco
    return localStorage.getItem("selectedColor") || "#ffffff";
  });

  useEffect(() => {
    // Guardar en localStorage cada vez que cambie
    localStorage.setItem("selectedColor", color);
  }, [color]);

  return (
    <div className="flex items-center justify-center h-full p-6">
      <div className="w-full max-w-md bg-white dark:bg-slate-800 rounded-2xl shadow-lg p-6 text-center">
        <h1 className="text-2xl font-bold text-slate-800 dark:text-slate-100 mb-6">
          🎨 Selector de Colores
        </h1>

        {/* Input tipo color */}
        <input
          type="color"
          value={color}
          onChange={(e) => setColor(e.target.value)}
          className="w-24 h-16 cursor-pointer border-2 border-slate-300 dark:border-slate-600 rounded-lg mb-6"
        />

        {/* Div que muestra el color */}
        <div
          className="w-full h-40 rounded-xl border-2 border-slate-200 dark:border-slate-700 shadow-inner"
          style={{ backgroundColor: color }}
        />
      </div>
    </div>
  );
}
