# -*- coding: utf-8 -*-
"""
Created on Tue Jul  4 15:51:41 2023

@author: Dyson

基础代码由AI提供：
帮我写个Python的服务，开启后监控特定的两类端口；
写端口：3个，数个端口共用一个“队列”，用于接收不同编码的数据和对应的表结构（元数据）；
写线程：将“队列”中的数据根据不同的表结构保存到不同的固定大小的文件（数据块）内，同时超过一定时间没更新的数据块也不再修改了。
读线程：管理“数据块”，将“数据块”的内容和对应的元数据读到内存里。
读端口：3个，从读线程获得数据，返回给需要的程序。
管理线程：监控每个“数据块”的文件大小，文件名，以及更新时间，同时整理不到固定大小的数据块。
每次访问端口，都要返回状态码，读端口的话，还有返回相应的数据。可以自定义保存数据块的路径。
"""

from loguru import logger
from pathlib import Path
import sys
py_dir = Path(__file__).parent
logger.configure(
    handlers=[
        # {"sink": "file.log", "format": "{time} {level} [{thread}] {message}"},
        {"sink": sys.stdout, "format": "{time:MM-DD HH:mm:ss} {level} [{thread}] {message}"}
    ]
)

import socket
import threading
import queue
import os
import time

# 定义常量
SERVER_ADDRESS = 'localhost'
WRITE_PORT_LIST = [8000, 8001, 8002]  # 写端口列表
READ_PORT_LIST = [9000, 9001, 9002]  # 读端口列表
QUEUE_SIZE = 100  # 队列大小
BLOCK_SIZE = 1024  # 数据块大小
MAX_BLOCK_TIME = 10  # 最大数据块时间（单位：秒）
MAX_BLOCK_SIZE = 10 * BLOCK_SIZE  # 最大数据块大小（单位：字节，这里设置为10个块）


# 初始化队列和数据块字典
data_queue = queue.Queue(maxsize=QUEUE_SIZE)
file_path = Path("./blocks")
block_dict = {}
meta_dict = {}

# 定义写线程类
class WriteThread(threading.Thread):
    def __init__(self, thread_id):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
    
    def run(self):
        while True:
            # 获取队列中的数据和对应的表结构
            data, meta_data = data_queue.get()
            # 获取线程对应的文件句柄
            if self.thread_id not in block_dict:
                block_dict[self.thread_id] = open(f'data_{self.thread_id}.txt', 'ab')
            f = block_dict[self.thread_id]
            # 将数据和元数据写入文件
            f.write(meta_data.encode() + b'\n' + data + b'\n')
            # 判断是否需要新建数据块
            if f.tell() >= BLOCK_SIZE:
                f.close()
                block_dict[self.thread_id] = open(f'data_{self.thread_id}.txt', 'ab')

# 定义读线程类
class ReadThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    
    def run(self):
        while True:
            # 循环遍历所有数据块
            for thread_id in block_dict:
                f = block_dict[thread_id]
                # 如果数据块非空，则读取数据和元数据
                if f.tell() > 0:
                    f.seek(0)
                    data_list = []
                    meta_data_list = []
                    while True:
                        meta_data = f.readline().decode().strip()
                        if not meta_data:
                            break
                        data = f.readline()
                        data_list.append(data)
                        meta_data_list.append(meta_data)
                    # 将数据和对应的元数据加入到字典中
                    block_dict[thread_id] = open(f'data_{thread_id}.txt', 'wb')
                    for i in range(len(data_list)):
                        data_queue.put((data_list[i], meta_data_list[i]))

# 定义管理线程类
class ManagerThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    
    def run(self):
        while True:
            # 循环遍历所有数据块
            for thread_id in block_dict:
                f = block_dict[thread_id]
                # 如果数据块存在且最近一次修改距离现在超过MAX_BLOCK_TIME秒，则打上标记
                if f.tell() > 0 and time.time()-os.path.getmtime(f.name) > MAX_BLOCK_TIME:
                    os.rename(f.name, f'{f.name}.marked')
                    block_dict[thread_id] = open(f'data_{thread_id}.txt', 'ab')
                # 如果数据块大小已经超出MAX_BLOCK_SIZE，则新建一个数据块
                if f.tell() >= MAX_BLOCK_SIZE:
                    block_dict[thread_id] = open(f'data_{thread_id}_{time.time()}.txt', 'wb')
            # 等待1秒钟
            time.sleep(1)

# 定义函数，用于处理客户端请求
def write_request(server_socket):
    thread_id = threading.current_thread().ident
    logger.info(f"线程{thread_id}：正在等待客户端连接...")
    

    while True:
        try:
            # 监听端口并处理请求
            conn, addr = server_socket.accept()
            print(f"线程{thread_id}：客户端已连接:{addr}")
            
            while True:
                request = conn.recv(1024)
                if not request:
                    break
                else:
                    print(f"线程{thread_id}：接受到请求:{request}")
                    
                # 返回状态码
                conn.send(b"200")
    
            # 关闭连接
            print(f"线程{thread_id}：完成传输，准备刷新")
            conn.close()
            # break
        except Exception as e:
            print("客户端连接异常:", e)
            conn.close()
            conn, addr = server_socket.accept()
            print("客户端已重新连接:", addr)
        
        
    # 根据请求类型进行处理
    # if data == b'get_status':
    #     status_code = 200
    #     response_data = b'service is running'
    # elif data.startswith(b'get_data'):
    #     # 获取线程ID，并向队列中加入请求
    #     thread_id = int(data.split()[1])
    #     data_queue.put((b'request', str(thread_id).encode() + b'\n'))
    #     # 从队列中获取响应
    #     response_data, meta_data = data_queue.get()
    #     status_code = 200
    # else:
    #     status_code = 400
    #     response_data = b'unsupported request type'
    # 发送响应
    # conn.sendall(str(200).encode())
    
# 定义函数，用于处理客户端请求
def read_request(server_socket):
    # 监听端口并处理请求
    conn, addr = server_socket.accept()
    # 读取客户端发送的数据
    data = conn.recv(1024)
    # 根据请求类型进行处理
    if data == b'get_status':
        status_code = 200
        response_data = b'service is running'
    elif data.startswith(b'get_data'):
        # 获取线程ID，并向队列中加入请求
        thread_id = int(data.split()[1])
        data_queue.put((b'request', str(thread_id).encode() + b'\n'))
        # 从队列中获取响应
        response_data, meta_data = data_queue.get()
        status_code = 200
    else:
        status_code = 400
        response_data = b'unsupported request type'
    # 发送响应
    conn.sendall(str(status_code).encode() + b'\n' + response_data)
    


# 启动服务
if __name__ == '__main__':
    if not file_path.exists():
        file_path.mkdir()
        
    logger.info("starting。sddddadsfsdfaddasfsadfsfsdafdffsd。......。")
        
    # 创建写线程
    for i in range(len(WRITE_PORT_LIST)):
        t = WriteThread(i)
        t.start()
    # 创建读线程
    rt = ReadThread()
    rt.start()
    # 创建管理线程
    mt = ManagerThread()
    mt.start()
    # 启动监听端口
    for port in READ_PORT_LIST:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((SERVER_ADDRESS, port))
        server_socket.listen(5)
        threading.Thread(target=read_request, args=(server_socket,)).start()
        
    for port in WRITE_PORT_LIST:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((SERVER_ADDRESS, port))
        server_socket.listen(5)
        threading.Thread(target=write_request, args=(server_socket,)).start()