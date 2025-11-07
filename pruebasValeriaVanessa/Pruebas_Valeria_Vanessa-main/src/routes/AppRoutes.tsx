// src/routes/AppRoutes.tsx
import { Routes, Route } from "react-router-dom";
import Layout from "../components/Layout";

// Views
import HomePage from "../views/HomePage";
import ThreeDemoView from "../views/ThreeDemoView";
import LayoutsView from "../views/LayoutsView";
import SpeechDemoView from "../views/SpeechDemoView";
import GeometryExplorer from "../views/GeometryExplorer";
import SettingsView from "../views/SettingsView";
import TablasMul from "../views/TablasMul";
import ConversorUnid from "../views/ConversorUnid";
import ValidContrasena from "../views/ValidContrasena";
import ContadorClics from "../views/ContadorClics";
import ListaTareas from "../views/ListaTareas";

// ✅ Nuevos Ejercicios
import DigitalClockView from "../views/DigitalClockView";
import CountdownTimerView from "../views/CountdownTimerView";
import ColorPickerView from "../views/ColorPickerView";
import SearchListView from "../views/SearchListView";

// 🌍 Nuevas vistas 3D
import GloboTerraqueo from "../views/GloboTerraqueoView";
import SistemaSolar from "../views/SistemaSolar";
import SimetriaFiguras from "../views/SimetriaFiguras";

export default function AppRoutes() {
  return (
    <Routes>
      <Route path="/" element={<Layout />}>
        {/* Menú Principal */}
        <Route index element={<HomePage />} />
        <Route path="three" element={<ThreeDemoView />} />
        <Route path="layouts" element={<LayoutsView />} />
        <Route path="tts" element={<SpeechDemoView />} />
        <Route path="three_2" element={<GeometryExplorer />} />
        <Route path="settings" element={<SettingsView />} />

        {/* Ejercicios existentes */}
        <Route path="tablasmul" element={<TablasMul />} />
        <Route path="conversorunid" element={<ConversorUnid />} />
        <Route path="validcontrasena" element={<ValidContrasena />} />
        <Route path="contadorclics" element={<ContadorClics />} />
        <Route path="listareas" element={<ListaTareas />} />

        {/* ✅ Nuevos Ejercicios */}
        <Route path="relojdigital" element={<DigitalClockView />} />
        <Route path="contadorregresivo" element={<CountdownTimerView />} />
        <Route path="selectorcolores" element={<ColorPickerView />} />
        <Route path="buscadorlista" element={<SearchListView />} />

        {/* 🌍 Nuevas vistas 3D */}
        <Route path="globo" element={<GloboTerraqueo />} />
        <Route path="sistemasolar" element={<SistemaSolar />} />
        <Route path="simetria" element={<SimetriaFiguras />} />
      </Route>
    </Routes>
  );
}
