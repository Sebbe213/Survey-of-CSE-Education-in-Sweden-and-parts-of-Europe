// vite.config.ts
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
export default defineConfig({
    plugins: [
        react() // ← use the import here!
    ],
    base: '/static/assets/',
    build: {
        outDir: '../server/static/assets',
        emptyOutDir: true,
        manifest: true,
        assetsDir: '.', // drop CSS/JS at the root of assets/
    },
});
