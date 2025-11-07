// src/components/Navbar.tsx
import React, { useEffect, useState } from "react";

const Navbar: React.FC = () => {
  const [themeIndex, setThemeIndex] = useState(0);
  const themes = ["light", "dark", "theme-rosa", "theme-verde"];

  useEffect(() => {
    const root = document.documentElement;
    const saved = localStorage.getItem("theme");
    const initialTheme = saved || "light";
    applyTheme(initialTheme);
  }, []);

  const applyTheme = (theme: string) => {
    const root = document.documentElement;
    root.classList.remove("light", "dark", "theme-rosa", "theme-verde");
    root.classList.add(theme);
    localStorage.setItem("theme", theme);
    document.dispatchEvent(new CustomEvent("theme:changed", { detail: { theme } }));
  };

  const toggleTheme = () => {
    const nextIndex = (themeIndex + 1) % themes.length;
    setThemeIndex(nextIndex);
    applyTheme(themes[nextIndex]);
  };

  return (
    <header className="h-14 sticky top-0 z-10 bg-white/70 dark:bg-slate-900/60 backdrop-blur border-b border-slate-200 dark:border-slate-800">
      <div className="container mx-auto px-4 h-full flex items-center justify-between">
        {/* Lado izquierdo: logo + marca */}
        <div className="flex items-center gap-2 font-semibold text-slate-800 dark:text-slate-100">
          <div className="inline-flex items-center justify-center w-8 h-8 rounded-lg bg-emerald-500 text-white">
            U
          </div>
          <span>UCC : Prácticas Desarrollo</span>
        </div>

        {/* Lado derecho: botón de tema */}
        <div className="flex items-center gap-2">
          <button
            type="button"
            onClick={toggleTheme}
            className="px-3 py-1.5 rounded-lg bg-slate-900 text-white dark:bg-slate-100 dark:text-slate-900 hover:opacity-90 transition"
          >
            Tema
          </button>
        </div>
      </div>
    </header>
  );
};

export default Navbar;
