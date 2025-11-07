// src/views/ColorPicker.tsx
import { useState, useEffect } from "react";

export default function ColorPicker() {
  const [color, setColor] = useState<string>(
    localStorage.getItem("color") || "#ffffff"
  );

  useEffect(() => {
    localStorage.setItem("color", color);
  }, [color]);

  return (
    <div className="flex items-center justify-center h-screen bg-gradient-to-br from-rose-100 via-pink-50 to-emerald-100">
      <div className="w-full max-w-md bg-white/70 backdrop-blur-lg rounded-3xl shadow-lg p-6 text-center border border-rose-200">
        <h1 className="text-2xl font-bold text-rose-600 mb-6">
          🎨 Selector de Colores
        </h1>
        <input
          aria-label="Seleccionar color"
          className="w-28 h-16 cursor-pointer border-2 border-slate-300 rounded-lg mb-6"
          type="color"
          value={color}
          onChange={(e) => setColor(e.target.value)}
        />
        <div
          data-testid="color-box"
          className="w-full h-40 rounded-xl border-2 border-slate-200 shadow-inner"
          style={{ backgroundColor: color }}
        />
      </div>
    </div>
  );
}
