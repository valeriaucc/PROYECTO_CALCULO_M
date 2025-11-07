import { Link, Outlet } from "react-router-dom";

export default function Layout() {
  return (
    <div className="flex h-screen bg-slate-50 dark:bg-slate-900">
      {/* Sidebar */}
      <aside className="w-64 bg-white dark:bg-slate-800 border-r border-slate-200 dark:border-slate-700 p-4">
        <h1 className="text-2xl font-bold text-slate-800 dark:text-slate-100 mb-6">
          🚀 JTest
        </h1>
        <nav>
          <ul className="space-y-3 text-slate-700 dark:text-slate-300">
            {/* Vistas antiguas */}
            <li><Link to="/" className="hover:text-indigo-500">🏠 Home</Link></li>
            <li><Link to="/tablasmul" className="hover:text-indigo-500">✖️ Tablas de Multiplicar</Link></li>
            <li><Link to="/conversorunid" className="hover:text-indigo-500">🔄 Conversor de Unidades</Link></li>
            <li><Link to="/validcontrasena" className="hover:text-indigo-500">🔑 Validar Contraseña</Link></li>
            <li><Link to="/contadorclics" className="hover:text-indigo-500">🖱️ Contador de Clics</Link></li>
            <li><Link to="/listareas" className="hover:text-indigo-500">📝 Lista de Tareas</Link></li>

            {/* Nuevos ejercicios */}
            <li><Link to="/clock" className="hover:text-indigo-500">🕒 Reloj Digital</Link></li>
            <li><Link to="/timer" className="hover:text-indigo-500">⏳ Contador Regresivo</Link></li>
            <li><Link to="/colors" className="hover:text-indigo-500">🎨 Selector de Colores</Link></li>
            <li><Link to="/search" className="hover:text-indigo-500">🔍 Buscador</Link></li>

            {/* Extras */}
            <li><Link to="/three" className="hover:text-indigo-500">🌐 Three.js Demo</Link></li>
            <li><Link to="/three_2" className="hover:text-indigo-500">📐 Geometry Explorer</Link></li>
            <li><Link to="/tts" className="hover:text-indigo-500">🗣️ Text-to-Speech</Link></li>
            <li><Link to="/settings" className="hover:text-indigo-500">⚙️ Settings</Link></li>
            <li><Link to="/layouts" className="hover:text-indigo-500">📦 Layouts</Link></li>
          </ul>
        </nav>
      </aside>

      {/* Contenido principal */}
      <main className="flex-1 p-6 overflow-y-auto">
        <Outlet />
      </main>
    </div>
  );
}
