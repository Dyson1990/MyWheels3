# -*- coding: utf-8 -*-
"""
Created on Fri Dec 16 17:11:54 2022

@author: Weave
"""
import sys
from pathlib import Path
py_dir = Path(__file__).parent

import paramiko
import contextlib
from loguru import logger

class SSHConnection:
    def __init__(self, host, username, passwd, port=22):
        self.host = host
        self.port = port
        self.username = username
        self.passwd = passwd
        
        self.conn = paramiko.SSHClient()
        # 允许连接不在know_hosts文件中的主机
        self.conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
    @contextlib.contextmanager
    def connection(self):
        logger.info("Opening SSH connection.")
        self.conn.connect(self.host
                          , username=self.username
                          , port=self.port
                          , password=self.passwd
                          )
        
        yield self # 类似于使用__enter__
        
        logger.info("Closing SSH connection.")
        self.conn.close()
        return None # 类似于使用__exit__
        
# =============================================================================
#     def __enter__(self):
#         # 建立连接
#         self.conn.connect(self.host, username=self.username, port=self.port, password=self.passwd)
#         # conn.connect("192.168.1.24", username="root", port=22, password="*ycy123*")
#         return self
#     
#     def __exit__(self, exc_type, exc_val, exc_tb):
#         self.conn.close()
# =============================================================================
        
    def __del__(self):
        # 关闭连接
        try:
            # 防止程序出错时，不断开连接？
            self.conn.close()
        except:
            pass
        
    def run_cmd(self, cmd, encoding="utf-8", file_output=None):
        stdin, stdout, stderr = self.conn.exec_command(f"bash -l -c '{cmd}'")
        # stdin, stdout, stderr = self.conn.exec_command(f"{cmd}", get_pty=False)
        if encoding:
            stdin_str = stdin.read().decode(encoding) if stdin.readable() else ""
            stdout_str = stdout.read().decode(encoding) if stdout.readable() else ""
            stderr_str = stderr.read().decode(encoding) if stderr.readable() else ""
        else:
            stdin_str = stdin.read() if stdin.readable() else b""
            stdout_str = stdout.read() if stdout.readable() else b""
            stderr_str = stderr.read() if stderr.readable() else b""
            
        return {"stdin":stdin_str, "stdout":stdout_str, "stderr":stderr_str}
            # return stdin, stdout, stderr
            
class SFTPConnection:
    def __init__(self, host, username, passwd, port=22):
        self.host = host
        self.port = port
        self.username = username
        self.passwd = passwd
        
        self.tran = paramiko.Transport((self.host, self.port))
        self.tran.connect(username=self.username, password=self.passwd)
        # 创建sftp实例
        self.sftp = paramiko.SFTPClient.from_transport(self.tran)

    @contextlib.contextmanager
    def connection(self):
        logger.info("Opening SFTP connection.")
        self.conn.connect(self.host
                          , username=self.username
                          , port=self.port
                          , password=self.passwd
                          )
        
        yield self # 类似于使用__enter__
        
        logger.info("Closing SFTP connection.")
        self.conn.close()
        return None # 类似于使用__exit__

# =============================================================================
#     def __enter__(self):
#         # 建立连接
#         self.conn.connect(self.host, username=self.username, port=self.port, password=self.passwd)
#         # conn.connect("192.168.1.24", username="root", port=22, password="*ycy123*")
#         return self
#     
#     def __exit__(self, exc_type, exc_val, exc_tb):
#         self.conn.close()
# =============================================================================
        
    def __del__(self):
        # 关闭连接
        try:
            # 防止程序出错时，不断开连接？
            self.conn.close()
        except:
            pass
        
    def put(self, local_p: Path, remote_p: Path):
        logger.info(f"准备上传文件{local_p}")
        return self.sftp.put(local_p, remote_p, confirm=True)
    
    def get(self, remote_p: Path, local_p: Path):
        logger.info(f"准备下载文件{remote_p}")
        return self.sftp.get(remotepath=remote_p, localpath=local_p)

if __name__ == "__main__":
    pass