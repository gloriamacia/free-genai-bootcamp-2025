import path from "path"
import react from "@vitejs/plugin-react"
import { defineConfig } from "vite"

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
  server: {
    proxy: {
      '/api': {
        target: 'http://34.205.203.251:5000',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, '') // non sure if this is necessary ASK DOUBT
      }
    }
  }
})