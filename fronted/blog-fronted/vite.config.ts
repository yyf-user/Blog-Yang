import { fileURLToPath, URL } from 'node:url';
import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';

export default defineConfig({
  plugins: [
    vue(),
  ],
  resolve: {
    alias: { '@': fileURLToPath(new URL('./src', import.meta.url)) }
  },
  // 开发环境优化
  server: {
    proxy: { 
      '/api': {
        target: 'http://localhost:8001',
        changeOrigin: true
      } 
    }
  }
});