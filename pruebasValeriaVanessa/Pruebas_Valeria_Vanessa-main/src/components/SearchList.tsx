// src/views/SearchList.tsx
import { useState } from "react";

const names = ["Ana", "Luis", "Carlos", "María", "Lucía", "Pedro", "Vanessa"];

export default function SearchList() {
  const [query, setQuery] = useState<string>("");

  const filteredNames = names.filter((name) =>
    name.toLowerCase().includes(query.toLowerCase())
  );

  return (
    <div className="flex items-center justify-center h-screen bg-gradient-to-br from-emerald-100 via-pink-100 to-rose-200">
      <div className="w-full max-w-md bg-white/70 backdrop-blur-lg rounded-3xl shadow-lg p-6 text-center border border-emerald-200">
        <h1 className="text-2xl font-bold text-emerald-600 mb-6">
          🔍 Buscador de Nombres
        </h1>
        <input
          type="text"
          placeholder="Escribe un nombre..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          className="w-full px-4 py-2 mb-6 border rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-400"
        />
        <ul className="text-lg text-slate-700 space-y-2">
          {filteredNames.length > 0 ? (
            filteredNames.map((name, idx) => <li key={idx}>{name}</li>)
          ) : (
            <li className="text-rose-500 font-semibold">No encontrado</li>
          )}
        </ul>
      </div>
    </div>
  );
}
