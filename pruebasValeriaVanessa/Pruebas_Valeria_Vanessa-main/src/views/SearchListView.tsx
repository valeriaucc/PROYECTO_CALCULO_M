// src/views/SearchList.tsx
import { useState } from "react";

export default function SearchList() {
  // Lista base de nombres
  const initialNames = [
    "Ana",
    "Carlos",
    "Pedro",
    "Lucía",
    "María",
    "Julián",
    "Sofía",
    "Mateo",
    "Camila",
    "Andrés",
  ];

  const [query, setQuery] = useState("");

  // Filtrado dinámico (insensible a mayúsculas/minúsculas)
  const filteredNames = initialNames.filter((name) =>
    name.toLowerCase().includes(query.toLowerCase())
  );

  return (
    <div className="flex items-center justify-center h-full p-6">
      <div className="w-full max-w-lg bg-white dark:bg-slate-800 rounded-2xl shadow-lg p-6">
        <h1 className="text-2xl font-bold text-slate-800 dark:text-slate-100 mb-6 text-center">
          🔍 Buscador en Lista
        </h1>

        {/* Input de búsqueda */}
        <input
          type="text"
          placeholder="Escribe un nombre..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          className="w-full px-4 py-2 mb-4 border border-slate-300 dark:border-slate-600 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:outline-none"
        />

        {/* Lista de resultados */}
        <div className="space-y-2">
          {filteredNames.length > 0 ? (
            filteredNames.map((name, index) => (
              <div
                key={index}
                className="p-3 rounded-lg border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-900 text-slate-700 dark:text-slate-300 hover:bg-emerald-50 dark:hover:bg-emerald-800/30 transition"
              >
                {name}
              </div>
            ))
          ) : (
            <p className="text-center text-red-500 font-semibold">
              ❌ No encontrado
            </p>
          )}
        </div>
      </div>
    </div>
  );
}
