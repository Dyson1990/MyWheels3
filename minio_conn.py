# -*- coding: utf-8 -*-
"""
Created on Mon Sep 19 17:10:25 2022

@author: Weave

单独通用脚本
"""

import minio

import os
import traceback
import re
import pathlib
import io
import time
import hashlib
from pathlib import Path
from tqdm import tqdm
from datetime import timedelta
from loguru import logger

# official: sudo docker run -p 9000:9000 --name minio   -v /var/lib/minio/data:/data   -v /var/lib/minio/config:/root/.minio   minio/minio server /data
# T430: docker run -p 9000:9000 -p 9090:9090 --net=host --name minio -d --restart=always -v /var/lib/minio/data:/data -v /var/lib/minio/config:/root/.minio minio/minio server /data --console-address ":19090" -address ":19000"
# h3: docker run -p 19000:9000 -p 19090:9090 --net=host --name minio -d --restart=always -v /mnt/data/minio:/data -v /var/lib/minio/config:/root/.minio minio/minio server /data --console-address ":19090" -address ":19000"
minio_cli = minio.Minio('192.168.1.23:19000',
                        access_key='minioadmin',
                        secret_key='minioadmin',
                        secure=False,
                        # http_client=httpClient
                        )

# buckets = minio_cli.list_buckets()
# print(buckets)

# bucket = minio_cli.bucket('test')
# minio_cli.fput_object('test', 'outter/a77999643350818e138c5093e3a2ebf3.html', r'C:\Users\Weave\crawler\opencorporates\content\a77999643350818e138c5093e3a2ebf3.html')

def put_string(content, object_name, bucket_name='etl', app_type='etl', chr_set='utf-8'):
    object_name = pathlib.Path(object_name)
    
    b0 = content.encode(chr_set)
    minio_cli.put_object(bucket_name
                         , object_name.as_posix()
                         , io.BytesIO(b0)
                         , len(b0)
                         , content_type=f'application/{app_type}'
                         )

def put_one_file(file_path, inner_dir, bucket_name='etl', app_type='etl'):
    """
    上传一整个文件夹的内容到minio
    Parameters
    ----------
    file_dir : TYPE
        本地文件夹的路劲.
    inner_dir : TYPE
        minio中，bucket内部的路径.
    bucket_name : TYPE, optional
        bucket名称. The default is 'crawler'.
    app_type : TYPE, optional
        应用类型. The default is 'crawler'.
    """
    file_path = pathlib.Path(file_path)
    inner_dir = pathlib.Path(inner_dir)
    
    object_name = inner_dir.joinpath(file_path.name).as_posix()
    minio_cli.fput_object(bucket_name
                          , object_name
                          , str(file_path)
                          , content_type=f'application/{app_type}'
                          )
    
def put_all_files(file_dir, inner_dir, bucket_name='etl', app_type='etl'):
    """
    上传一整个文件夹的内容到minio
    Parameters
    ----------
    file_dir : TYPE
        本地文件夹的路劲.
    inner_dir : TYPE
        minio中，bucket内部的路径.
    bucket_name : TYPE, optional
        bucket名称. The default is 'crawler'.
    app_type : TYPE, optional
        应用类型. The default is 'crawler'.

    Returns
    -------
    None.

    """
    file_dir = pathlib.Path(file_dir)
    inner_dir = pathlib.Path(inner_dir)
    for file_path in tqdm(list(file_dir.iterdir())):
        object_name = inner_dir.joinpath(file_path.name).as_posix()

        minio_cli.fput_object(bucket_name
                              , object_name
                              , str(file_path)
                              , content_type=f'application/{app_type}'
                              )
        
def get_file(object_name, bucket_name='etl'):
    """
    由于读取不存在的obj会报错，这里增加一个读取的函数
    """
    try:
        # print(type(bucket_name), type(object_name))
        obj = minio_cli.get_object(bucket_name, object_name)
        return obj.read().decode('utf-8')
    except minio.error.S3Error as e:
        if e.code == 'NoSuchKey':
            return None
        else:
            raise minio.error.S3Error(str(e))
            
def get_url(object_name, expiry=timedelta(days=1), bucket_name='etl'):
    """
    由于读取不存在的obj会报错，这里增加一个读取的函数
    """
    try:
        obj = minio_cli.presigned_get_object(bucket_name, object_name)
        return obj
    except minio.error.S3Error as e:
        if e.code == 'NoSuchKey':
            return None
        else:
            print(e.code)
            raise minio.error.S3Error(str(e))
            
def empty_bucket(bucket_name='etl'):
    warning = input('真的要清空：'+bucket_name+'?【Y/N】')
    if warning == 'Y':
        for obj in minio_cli.list_objects(bucket_name, prefix='opencorporates/html/content'):
            print('正在删除：', obj.object_name)
            # break
            minio_cli.remove_object(obj.bucket_name, obj.object_name)
            
def search_file(search_str, regex=False, prefix=None, allow_dups=False, bucket_name='etl'):
    obj_list = minio_cli.list_objects(bucket_name, prefix=prefix, recursive=True)
    if regex:
        obj_str = "\n".join([obj.object_name for obj in obj_list])
        res = re.findall(search_str, obj_str, re.M)
    else:
        res = []
        for obj in obj_list:
            if obj.object_name.endswith(search_str):
                res.append(obj.object_name)
                
    if len(res) > 1 and allow_dups == False:
        raise Exception(f"{search_str}存在多个结果：{res}，需要调整！")
    elif len(res) == 1 and allow_dups == False:
        return Path(res.pop())
    else:
        return [Path(s0) for s0 in res]
        
    logger.warning("没有找到所需结果！")
    return None
            
def sync_one_file(local_fp:Path, minio_fp:Path, bucket_name='etl'
                  , auth=None, rename=None):
    # print(minio_fp)
    minio_dir, minio_fn = os.path.split(minio_fp)
    
    if local_fp.is_dir():
        raise Exception('本地路径指向文件夹了，需要是文件路径！')
    if minio_fn != local_fp.name:
        raise Exception(f"minio上的文件名({minio_fn})与本地({local_fp.name})不相同，请确定是不是同步目标，是的话请修改文件名！")
    
    local_exists = local_fp.exists()
    minio_exists = bool(get_file(minio_fp.as_posix(), bucket_name=bucket_name))
    if not local_exists and not minio_exists:
        raise Exception(f'本地【{local_fp}】与minio【{minio_fp}】上的路径都不存在！')
    elif local_exists and not minio_exists:
        if auth == "upload":
            # print("minio_dir:", type(minio_dir), minio_dir)
            put_one_file(local_fp, minio_dir, bucket_name=bucket_name)
            logger.info(f'minio【{minio_fp}】不存在，已从本地上传！')
        else:
            logger.info(f'minio【{minio_fp}】不存在，请检查！')
        return None
    elif not local_exists and minio_exists:
        if auth == "download":
            content = get_file(minio_fp.as_posix(), bucket_name=bucket_name)
            local_dir = local_fp.parent
            if not local_dir.exists():
                local_dir.mkdir()
            local_fp.write_text(content, encoding='UTF-8')
            logger.info(f'本地文件【{local_fp}】不存在，已从minio上下载！')
        else:
            logger.info(f'本地文件【{local_fp}】不存在，请检查！')
        return None
    
    fn = local_fp.name
    minio_obj = minio_cli.get_object(bucket_name, minio_fp.as_posix())
    minio_update_time = time.strptime(minio_obj.getheader('Last-Modified')
                                      , '%a, %d %b %Y %H:%M:%S %Z')
    local_update_time = time.localtime(local_fp.lstat().st_mtime)
    
    local_md5 = hashlib.md5(local_fp.read_bytes()).digest()
    minio_md5 = hashlib.md5(minio_obj.read()).digest()

    if local_md5 == minio_md5:
        pass
    elif minio_update_time < local_update_time:
        bak_object_name = "ktr/"+time.strftime("%Y%m%d%H%M%S", local_update_time)
        # minio_cli.copy_object("backup", object_name, "/test/"+minio_fp)
        # 暂时用笨方法备份
        content = get_file(minio_fp.as_posix(), bucket_name=bucket_name)
        tmp_path = Path(f"./{fn}.bak")
        tmp_path.write_text(content, encoding='UTF-8')
        put_one_file(tmp_path, bak_object_name, bucket_name="backup")
        os.remove(tmp_path)
        
        put_one_file(local_fp, minio_dir, bucket_name=bucket_name)
        logger.info(f'已将本地文件({fn})上传至minio')
    elif minio_update_time > local_update_time:
        content = get_file(minio_fp.as_posix(), bucket_name=bucket_name)
        put_one_file(local_fp, "ktr/"+time.strftime("%Y%m%d%H%M%S", minio_update_time), bucket_name="backup")
        local_fp.write_text(content, encoding='UTF-8')
        logger.info(f'已将minio文件({fn})同步至本地')
    
    return None
        
def sync_dir(local_dir:Path, minio_dir:Path, bucket_name='etl', auth=None):
    if local_dir.is_file():
        raise Exception('本地路径指向文件了，需要是文件夹路径！')
    
    checked_file = []
    for p0 in local_dir.rglob("*"):
        if p0.is_file():
            s1 = p0.as_posix()
            s2 = local_dir.as_posix()
            if s1.startswith(s2):
                relative_p = s1[len(s2)+1:]
                minio_fp = minio_dir.joinpath(relative_p)
                # print("WTF", minio_dir, relative_p, minio_fp)
                sync_one_file(p0, minio_fp, bucket_name=bucket_name, auth=auth)
            else:
                logger.error(f"文件路径：{s1}跟目录{s2}冲突")
        checked_file.append(p0)

    obj_list = minio_cli.list_objects(bucket_name, prefix=minio_dir.as_posix(), recursive=True)
    for obj in obj_list:
        minio_fp = obj.object_name # .encode('utf-8')
        p0, minio_fn = os.path.split(minio_fp)
        
        if p0.startswith(minio_dir.as_posix()):
            relative_dir_str = p0[len(minio_dir.as_posix()):]
            if relative_dir_str.startswith("/"):
                relative_dir_str = relative_dir_str[1:]
                
            relative_dir = Path(relative_dir_str)
        else:
            logger.error(f"目录：{minio_dir}跟目录：{p0}冲突")
            
        local_fp = local_dir/relative_dir/minio_fn
        minio_fp = relative_dir/minio_fn
        # print("local_fp", local_fp)
        # print("minio_fp", minio_fp)
        
        if local_fp in checked_file:
            continue
        
        sync_one_file(local_fp, minio_fp, bucket_name=bucket_name, auth=auth)
        
        # print(obj.bucket_name, obj.object_name.encode('utf-8'), obj.last_modified,
        #       obj.etag, obj.size, obj.content_type)
        

    
    
if __name__ == '__main__':
    # search_file("")
    sync_dir(Path(r'C:\Users\Weave\Desktop\易查云\资源库\pdi_local')
             , Path('pdi/ktr')
             , bucket_name='etl'
             , auth="upload"
             )
    # sync_one_file(Path(r'C:\Users\Weave\Desktop\易查云\资源库\pdi\test1.ktr')
    #               , Path('p1/test1.ktr')
    #               , bucket_name='test'
    #               )
    
    # help(minio_cli.fput_object)
    # put_all_files(r'C:\Users\Weave\crawler\opencorporates\catalog'
    #               , 'opencorporates/html/catalog'
    #               )
    
    # put_all_files(r'C:\Users\Weave\crawler\opencorporates\content'
    #               , 'opencorporates/html/content'
    #               )
    # obj = get_file('opencorporates/html/content\f66c6dd53e09b3df42a9fb219635312f.html')
    # print(obj)
    # p0 = pathlib.Path('opencorporates/html/content')
    # print()
    # empty_bucket()
    # minio_cli.remove_objects('crawler', minio_cli.list_objects('crawler', prefix='opencorporates/html/catalog/'))
    # help(minio_cli.put_object)
    # output = Stream('abc')
    # minio_cli.put_object('test', 'p/abc.txt', io.BytesIO(b"hello"), len(b"hello"))
    # resp = put_string('dsafsadfsd', 'p1/https://blog.csdn.net/wsjslient/article/details/109743495', bucket_name='test')
    # print('resp', resp)
    # print(get_url('opencorporates/html/catalog/00000447d9398d84f2747d80a411875b.html'))
    
    
    