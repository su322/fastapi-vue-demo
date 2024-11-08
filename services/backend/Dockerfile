# 使用 python:3.11-buster 作为基础镜像
FROM python:3.11-buster

# 创建应用目录
RUN mkdir app

# 设置工作目录为 /app
WORKDIR /app

# 设置环境变量
ENV PATH="${PATH}:/root/.local/bin"
ENV PYTHONPATH=.

# 复制 requirements.txt 文件到工作目录
COPY requirements.txt .

# 升级 pip
RUN pip install --upgrade pip

# 安装依赖
RUN pip install -r requirements.txt

# 复制 src 目录下的所有文件到工作目录
COPY src/ .