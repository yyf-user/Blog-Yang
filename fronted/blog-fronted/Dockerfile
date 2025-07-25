# ---------- build stage ----------
FROM node:18.19 AS build-stage

WORKDIR /app

# 1. 依赖描述文件
COPY package*.json ./
COPY tsconfig*.json ./

# 2. 安装全部依赖 + 构建期必用插件
RUN npm ci --include=dev && \
    npm install -D \
        esbuild@0.21.5 \
        @tsconfig/node18 \
        rollup-plugin-visualizer \
        vite-plugin-compression \
        unplugin-auto-import \
        unplugin-vue-components \
        terser

# 3. 源码
COPY . .

# 4. 构建
RUN npm run build

# ---------- production stage ----------
FROM nginx:stable-alpine AS production-stage

COPY --from=build-stage /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf


EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]