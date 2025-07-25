FROM python:3.13-slim

WORKDIR /app  # 容器内的工作目录是 /app

# 复制项目文件（将主机 backend 目录下的所有内容复制到容器 /app 下）
COPY . .

# 安装依赖（requirements.txt 现在位于 /app 中）
RUN pip install --no-cache-dir -r requirements.txt

# 创建上传目录
RUN mkdir -p app/uploads/avatars app/uploads/images

# 暴露端口
EXPOSE 8000

# 启动命令
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]