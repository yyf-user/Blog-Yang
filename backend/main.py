"""
主应用入口点

此文件是应用的主入口点，负责启动FastAPI服务器。
"""
import os
import sys
import uvicorn
import argparse

def main():
    # 解析命令行参数
    parser = argparse.ArgumentParser(description="博客系统后端服务")
    parser.add_argument("--create-sample-data", action="store_true", help="创建示例API统计数据")
    parser.add_argument("--fix-database", action="store_true", help="修复数据库问题")
    args = parser.parse_args()
    
    # 构建启动命令
    cmd_args = []
    if args.create_sample_data:
        cmd_args.append("--create-sample-data")
    if args.fix_database:
        cmd_args.append("--fix-database")
    
    # 启动Uvicorn服务器
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )

if __name__ == "__main__":
    main() 