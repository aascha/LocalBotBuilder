import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    proxy: {
      '/api': {
        target: 'http://bot_creator:5000',  // ✅ Use Docker Compose service name
        changeOrigin: true,
        secure: false,
      }
    }
  }
})
