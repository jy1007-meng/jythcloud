import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  // 构建输出到网站根目录
  base: '/',
  build: {
    outDir: '../dist',
    emptyOutDir: true,
    // 生成 index.html 用作首页
    rollupOptions: {
      output: {
        // JS/CSS 命名带 hash 防缓存
        entryFileNames: 'assets/[name].[hash].js',
        chunkFileNames: 'assets/[name].[hash].js',
        assetFileNames: 'assets/[name].[hash][extname]',
      }
    }
  }
})
