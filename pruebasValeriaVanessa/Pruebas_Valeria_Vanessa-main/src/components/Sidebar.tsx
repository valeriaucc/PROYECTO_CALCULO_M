// src/components/Sidebar.tsx
import { useState } from "react";
import { NavLink } from "react-router-dom";
import { FaGlobeAmericas, FaSun, FaShapes } from "react-icons/fa";

interface SidebarItem {
  label: string;
  route: string;
  icon?: React.ReactNode;
}

const threeDItems: SidebarItem[] = [
  { label: "Globo Terráqueo", route: "/globo", icon: <FaGlobeAmericas /> },
  { label: "Sistema Solar", route: "/sistemasolar", icon: <FaSun /> },
  { label: "Simetría de Figuras", route: "/simetria", icon: <FaShapes /> },
];

export default function Sidebar() {
  const [open, setOpen] = useState(true);

  const renderNavItem = ({ label, route, icon }: SidebarItem) => (
    <NavLink
      key={route}
      to={route}
      className={({ isActive }) =>
        `relative w-full flex items-center gap-3 px-3 py-2 rounded-lg transition-colors duration-200 
         hover:bg-emerald-50 dark:hover:bg-slate-800 
         ${
           isActive
             ? "bg-emerald-100 text-emerald-700 dark:bg-emerald-900/30 dark:text-emerald-300 font-medium"
             : "text-slate-700 dark:text-slate-300"
         }`
      }
    >
      <span className="text-lg">{icon}</span>
      <span className="truncate">{label}</span>
    </NavLink>
  );

  return (
    <aside className="hidden md:block w-full md:w-[260px] border-r border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900">
      <div className="p-4 space-y-2">
        {/* Sección 3D */}
        <button
          onClick={() => setOpen(!open)}
          className="w-full flex items-center justify-between text-slate-700 dark:text-slate-300 font-semibold px-3 py-2 hover:bg-slate-100 dark:hover:bg-slate-800 rounded-lg"
        >
          Experimentos 3D
          <span>{open ? "▲" : "▼"}</span>
        </button>

        {open && <div className="pl-3 space-y-1">{threeDItems.map(renderNavItem)}</div>}
      </div>
    </aside>
  );
}
