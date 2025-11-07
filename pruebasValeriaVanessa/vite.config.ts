import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import path from "path";

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
  server: {
    hmr: {
      overlay: false, // Desactiva el error rojo en pantalla
    },
  },
  optimizeDeps: {
    esbuildOptions: {
      tsconfig: path.resolve(__dirname, "tsconfig.node.json"), // Forzamos la ruta correcta
    },
  },
});
