# 使用官方Python运行时作为父镜像
FROM python:3.10-slim-buster

# 设置工作目录
WORKDIR /app

# 将当前目录内容复制到容器的/app中
ADD . /app

RUN pip install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple
# 安装程序需要的包
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 运行时监听的端口
EXPOSE 8000

# 设置默认运行参数

# 指定使用的推理设备。例如，'cpu' or 'cuda:0'
ENV DEVICE cpu 

# 指定 Milvus 数据库地址
ENV MILVUS_URI http://localhost:19530

# 指定
ENV NAME_LIST ["command", "url", "payload"]

# 运行容器时的命令及其参数
ENTRYPOINT ["uvicorn", "api:app", "--reload"]