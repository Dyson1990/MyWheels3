# -*- coding: utf-8 -*-
"""
Created on Fri Dec 16 17:11:54 2022

@author: Weave
"""
import sys
from pathlib import Path
py_dir = Path(__file__).parent

import paramiko
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
        # 建立连接

        
    def __enter__(self):
        self.conn.connect(self.host, username=self.username, port=self.port, password=self.passwd)
        # conn.connect("192.168.1.24", username="root", port=22, password="*ycy123*")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()
        
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

    def __del__(self):
        # 关闭连接
        self.tran.close()
        
    def put(self, local_p: Path, remote_p: Path):
        logger.info(f"准备上传文件{local_p}")
        return self.sftp.put(local_p, remote_p, confirm=True)
    
    def get(self, remote_p: Path, local_p: Path):
        logger.info(f"准备下载文件{remote_p}")
        return self.sftp.get(remotepath=remote_p, localpath=local_p)
            
class SSHConnectionH4(SSHConnection):
    def __init__(self): # , host="192.168.1.24", username="root", passwd="*ycy123*", port=22
        super(SSHConnectionH4,self).__init__("192.168.1.24", "root", "*ycy123*")
        
class SSHConnectionH3(SSHConnection):
    def __init__(self):
        super(SSHConnectionH3,self).__init__("192.168.1.23", "root", "*ycy123*")


if __name__ == "__main__":
    # ssh = SSHConnectionH3()
    # resp = ssh.run_cmd("mysql -h192.168.1.23 -P13307 -uroot -proot -e \"use logic_db;DROP TABLE ODS_DV56\"")
    # print(resp["stderr"])
    
    sftp = SFTPConnection("192.168.1.24", "root", "*ycy123*")
    ktr_manager_dir = Path("/root/Documents/ktr_manager")
    sftp.put(py_dir/"流程管理表.xlsx"
             , (ktr_manager_dir/"流程管理表.xlsx").as_posix()
             )
    sftp.put(py_dir/"run_kjb.py"
             , (ktr_manager_dir/"run_kjb.py").as_posix()
             )
    sftp.put(Path("D:\Program Files (x86)\data-integration\.kettle\shared.xml")
             , Path("/usr/share/data-integration/.kettle/shared.xml").as_posix()
             )
    sftp.put(Path("D:\Program Files (x86)\data-integration\.kettle\shared.xml")
             , Path("/root/.kettle/shared.xml").as_posix()
             )
    # sftp.put(Path("D:\Program Files (x86)\data-integration\.kettle\shared.xml")
    #          , Path("/home/yichayun004/Documents/ktr_manager/ktr_flow/ODS_DV56/RU_BE_201908_EXP/log/shared.xml").as_posix()
    #          )

    ssh = SSHConnectionH4()
    tn = "RU_BE_202002_IMP_C1"
    cmd = f"python3 {ktr_manager_dir.as_posix()}/run_kjb.py {tn}"
    logger.info(cmd)
    resp = ssh.run_cmd(cmd)
    # resp = ssh.run_cmd("/usr/share/data-integration/kitchen.sh /file:/home/yichayun004/Documents/ktr_manager/ktr_flow/ODS_DV56/RU_BE_201908_EXP/流程调用.kjb /logfile:/home/yichayun004/Documents/ktr_manager/ktr_flow/ODS_DV56/RU_BE_201908_EXP/log/kjb.log /norep")
    # resp = ssh.run_cmd("echo JAVA_HOME=$JAVA_HOME")
    
    if resp["stdin"]:
        (py_dir/"ssh_log"/f"{tn}_stdin.log").write_text(resp["stdin"], encoding="utf-8")
    if resp["stdout"]:
        (py_dir/"ssh_log"/f"{tn}_stdout.log").write_text(resp["stdout"], encoding="utf-8")
    if resp["stderr"]:
        (py_dir/"ssh_log"/f"{tn}_stderr.log").write_text(resp["stderr"], encoding="utf-8")