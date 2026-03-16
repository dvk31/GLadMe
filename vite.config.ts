import { resolve } from "node:path";
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  root: resolve(__dirname, "frontend"),
  base: "/static/",
  resolve: {
    alias: {
      "@": resolve(__dirname, "frontend"),
    },
  },
  build: {
    outDir: resolve(__dirname, "static", "dist"),
    manifest: "manifest.json",
    emptyOutDir: true,
    rollupOptions: {
      input: resolve(__dirname, "frontend", "main.tsx"),
    },
  },
  server: {
    port: 5173,
    strictPort: true,
  },
});
