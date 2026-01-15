import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'path';

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
      '@/core': path.resolve(__dirname, './src/core'),
      '@/domains': path.resolve(__dirname, './src/domains'),
    },
  },
  server: {
    // 3000번 대신 5173(Vite 기본) 사용 (변경 필요 시 port: 3000 추가)
    proxy: {
      // 1. 신규 API (FastAPI)
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
      // 2. 레거시 컨트롤러 요청 (.do)
      // 정규식: .do로 끝나는 모든 요청을 8080으로 보냄
      '^/.*\\.do$': {
        target: 'http://localhost:8080',
        changeOrigin: true,
        secure: false,
      },
      // 3. 레거시 정적 리소스 
      '/css': { target: 'http://localhost:8080', changeOrigin: true },
      '/js': { target: 'http://localhost:8080', changeOrigin: true },
      '/img': { target: 'http://localhost:8080', changeOrigin: true },
      '/images': { target: 'http://localhost:8080', changeOrigin: true },
      '/lib': { target: 'http://localhost:8080', changeOrigin: true },
      '/common': { target: 'http://localhost:8080', changeOrigin: true },
      '/font': { target: 'http://localhost:8080', changeOrigin: true },
      '/dist': { target: 'http://localhost:8080', changeOrigin: true },
    }
  }
});
