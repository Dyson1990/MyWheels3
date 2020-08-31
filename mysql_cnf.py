# -*- coding: utf-8 -*-
"""
Created on Tue Aug  4 09:58:16 2020

@author: gooddata
"""

import psutil
import codecs

mysqld_args = {
    "character-set-client-handshake": "FALSE",
    "character-set-server": "utf8mb4",
    "collation-server": "utf8mb4_unicode_ci",
    # "init_connect": "SET NAMES utf8mb4",
    "skip-name-resolve": "1",
    "binlog_expire_logs_seconds": "7",

 
# 如果MySql的连接数据达到max_connections时，新来的请求将会被存在堆栈中，以等待某一连接释放资源，
# 该堆栈的数量即back_log，如果等待连接的数量超过back_log，将不被授予连接资源。
 
    "back_log": "600",

 
# 如果服务器的并发连接请求量比较大，建议调高此值，以增加并行连接数量，当然这建立在机器能支撑的情况下，
# 因为如果连接数越多，介于MySql会为每个连接提供连接缓冲区，就会开销越多的内存，所以要适当调整该值，
# 不能盲目提高设值。可以过'conn%'通配符查看当前状态的连接数量，以定夺该值的大小。
 
    "max_connections": "8000",
    "max_connect_errors": "10000",
    # 设置为0表示不限制。
    "max_user_connections": "30",

    "open_files_limit": "10240",

    # 弃用"thread_concurrency": int(psutil.cpu_count() * 2),

    # 网络传输中一次消息传输量的最大值。系统默认值 为1MB，最大值是1GB，必须设置1024的倍数。
    "max_allowed_packet": "1GB",

 
# 每个客户端线程和连接缓存和结果缓存交互，每个缓存最初都被分配大小为net_buffer_length的容量，
# 并动态增长，直至达到max_allowed_packet参数的大小。
 
    "net_buffer_length": "1MB",

 
# 服务器关闭交互式连接前等待活动的秒数。
# 交互式客户端定义为在mysql_real_connect()中使用CLIENT_INTERACTIVE选项的客户端。
 
    "interactive_timeout": 30 * 60,

 
# 服务器关闭非交互连接之前等待活动的秒数。在线程启动时，
# 根据全局wait_timeout值或全局 interactive_timeout值初始化会话wait_timeout值，
# 取决于客户端类型(由mysql_real_connect()的连接选项CLIENT_INTERACTIVE定义).
 
    "wait_timeout": 2 * 60 *60,

 
# 默认的thread_cache_size=8，但是看到好多配置的样例里的值一般是32，64，甚至是128，感觉这个参数对优化应该有帮助，于是查了下：
# 根据调查发现以上服务器线程缓存thread_cache_size没有进行设置，或者设置过小,这个值表示可以重新利用保存在缓存中线程的数量,当断开连接时如果缓存中还有空间,那么客户端的线程将被放到缓存中,如果线程重新被请求，那么请求将从缓存中读取,如果缓存中是空的或者是新的请求，那么这个线程将被重新创建,如果有很多新的线程，增加这个值可以改善系统性能.通过比较 Connections 和 Threads_created 状态的变量，可以看到这个变量的作用。(–>表示要调整的值)   根据物理内存设置规则如下：
# 1G —> 8
# 2G —> 16
# 3G —> 32     >3G —> 64
# 
#  mysql> show status like 'thread%';
# +——————-+——-+
# | Variable_name     | Value |
# +——————-+——-+
# | Threads_cached    | 0     |  <—当前被缓存的空闲线程的数量
# | Threads_connected | 1     |  <—正在使用（处于连接状态）的线程
# | Threads_created   | 1498  |  <—服务启动以来，创建了多少个线程
# | Threads_running   | 1     |  <—正在忙的线程（正在查询数据，传输数据等等操作）
# +——————-+——-+
# 
# 查看开机起来数据库被连接了多少次？
# 
# mysql> show status like '%connection%';
# +———————-+——-+
# | Variable_name        | Value |
# +———————-+——-+
# | Connections          | 1504  |          –>服务启动以来，历史连接数
# | Max_used_connections | 2     |
# +———————-+——-+
# 
# 通过连接线程池的命中率来判断设置值是否合适？命中率超过90%以上,设定合理。
# (Connections -  Threads_created) / Connections * 100 %
 
    "thread_cache_size": "85",
    
    # 是否开启慢查询日志，1表示开启，0表示关闭。
    "slow_query_log": "1",
    "slow_query_log_file": "/tmp/mysql/mysql-slow.log",
    # 慢查询阈值，当查询时间多于设定的阈值时，记录日志。
    "long_query_time": "600",
    
    # connection级参数。太大将导致在连接数增高时，内存不足。
    "sort_buffer_size": "16M",
    
 
# MySql读入缓冲区大小。对表进行顺序扫描的请求将分配一个读入缓冲区，MySql会为它分配一段内存缓冲区。
# read_buffer_size变量控制这一缓冲区的大小。如果对表的顺序扫描请求非常频繁，
# 并且你认为频繁扫描进行得太慢，可以通过增加该变量值以及内存缓冲区大小提高其性能.
 
    "read_buffer_size": "16M",

 
# MySql的随机读缓冲区大小。当按任意顺序读取行时(例如，按照排序顺序)，将分配一个随机读缓存区。
# 进行排序查询时，MySql会首先扫描一遍该缓冲，以避免磁盘搜索，提高查询速度，如果需要排序大量数据，
# 可适当调高该值。但MySql会为每个客户连接发放该缓冲空间，所以应尽量适当设置该值，以避免内存开销过大。
 
    "read_rnd_buffer_size": "32M",
    # 该参数对应的分配内存也是每个连接独享
    "join_buffer_size": "128M",

 
# MySql的heap （堆积）表缓冲大小。所有联合在一个DML指令内完成，
# 并且大多数联合甚至可以不用临时表即可以完成。大多数临时表是基于内存的(HEAP)表。
# 具有大的记录长度的临时表 (所有列的长度的和)或包含BLOB列的表存储在硬盘上。
# 如果某个内部heap（堆积）表大小超过tmp_table_size，
# MySQL可以根据需要自动将内存中的heap表改为基于硬盘的MyISAM表。
# 还可以通过设置tmp_table_size选项来增加临时表的大小。也就是说，如果调高该值，
# MySql同时将增加heap表的大小，可达到提高联接查询速度的效果。
 
    "tmp_table_size": "128M",
    
    # 索引的缓冲区大小，对于内存在4GB左右的服务器来说，该参数可设置为256MB或384MB。
    "key_buffer_size": int(psutil.virtual_memory().total / 16),
    
 
# query_cache_size: 主要用来缓存MySQL中的ResultSet，也就是一条SQL语句执行的结果集，
# 所以仅仅只能针对select语句。当我们打开了 Query Cache功能，MySQL在接受到一条select语句的请求后，
# 如果该语句满足Query Cache的要求(未显式说明不允许使用Query Cache，
# 或者已经显式申明需要使用Query Cache)，MySQL会直接根据预先设定好的HASH算法将接受到的select语句以字符串方式进行hash，
# 然后到Query Cache中直接查找是否已经缓存。也就是说，如果已经在缓存中，该select请求就会直接将数据返回，
# 从而省略了后面所有的步骤(如SQL语句的解析，优化器优化以及向存储引擎请求数据等)，极大的提高性能。
# 根据MySQL用户手册，使用查询缓冲最多可以达到238%的效率。
# 
# 当然，Query Cache也有一个致命的缺陷，那就是当某个表的数据有任何任何变化，
# 都会导致所有引用了该表的select语句在Query Cache中的缓存数据失效。
# 所以，当我们的数据变化非常频繁的情况下，使用Query Cache可能会得不偿失Query Cache的使用需要多个参数配合，
# 其中最为关键的是query_cache_size和query_cache_type，前者设置用于缓存 ResultSet的内存大小，
# 后者设置在何场景下使用Query Cache。在以往的经验来看，如果不是用来缓存基本不变的数据的MySQL数据库，
# query_cache_size一般256MB是一个比较合适的大小。当然，
# 这可以通过计算Query Cache的命中率(Qcache_hits/(Qcache_hits+Qcache_inserts)*100))来进行调整。 
# query_cache_type可以设置为0(OFF)，1(ON)或者2(DEMOND)，分别表示完全不使用query cache，
# 除显式要求不使用query cache(使用sql_no_cache)之外的所有的select都使用query cache，
# 只有显示要求才使用query cache(使用sql_cache)。如果Qcache_lowmem_prunes的值非常大，则表明经常出现缓冲. 
# 如果Qcache_hits的值也非常大，则表明查询缓冲使用非常频繁，此时需要增加缓冲大小；
# 
# 根据命中率(Qcache_hits/(Qcache_hits+Qcache_inserts)*100))进行调整，一般不建议太大，
# 256MB可能已经差不多了，大型的配置型静态数据可适当调大.
# 
# 可以通过命令：show status like 'Qcache_%';查看目前系统Query catch使用大小
# 
# | Qcache_hits             | 1892463  |
# 
# | Qcache_inserts          | 35627  
# 
# 命中率98.17%=1892463/(1892463 +35627 )*100
 
    # 弃用"query_cache_size": "256MB",
    
    # 每个线程的堆栈大小，默认值足够大，可满足普通操作。可设置范围为128K至4GB，默认为192KB。
    "thread_stack": "512K",


# 只需要用Innodb的话则可以设置它高达 70-80% 的可用内存。一些应用于 key_buffer 的规则有 ——如果你的数据量不大，
# 并且不会暴增，那么无需把innodb_buffer_pool_size 设置的太大了。

    "innodb_buffer_pool_size": int(psutil.virtual_memory().total * 0.7),
    
    # 网络传输中一次消息传输量的最大值。系统默认值为1MB，最大值是1GB，必须设置1024的倍数。
    # 弃用"innodb_additional_mem_pool_size": "16M",
    
    "innodb_read_io_threads": int(psutil.cpu_count() * 2),
    "innodb_write_io_threads": int(psutil.cpu_count() * 2),
    # "innodb_thread_concurrency": "16",
    
 
# InnoDB 将日志写入日志磁盘文件前的缓冲大小。理想值为 1M 至 8M。
# 大的日志缓冲允许事务运行时不需要将日志保存入磁盘而只到事务被提交(commit)。 
# 因此，如果有大的事务处理，设置大的日志缓冲可以减少磁盘I/O。 
 
    "innodb_log_buffer_size": "16M",
    
    "innodb_log_file_size": "512M",
    "innodb_log_files_in_group": "3",
    "innodb_lock_wait_timeout": "120",
    
    "datadir": "/disk_1t/mysql/",
    "socket": "/var/lib/mysql/mysqld.sock",
    "pid-file": "/var/lib/mysql/mysqld.pid",
    "log-error": "/var/log/mysql/error.log",
    "log-bin": "/var/lib/mysql/log_bin",
    "activate_all_roles_on_login": "ON",
}

mysqld_info =  """
# Copyright (c) 2014, 2017, Oracle and/or its affiliates. All rights reserved.
# 
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License, version 2.0,
# as published by the Free Software Foundation.
# 
# This program is also distributed with certain software (including
# but not limited to OpenSSL) that is licensed under separate terms,
# as designated in a particular file or component or in included license
# documentation.  The authors of MySQL hereby grant you an additional
# permission to link the program and your derivative works with the
# separately licensed software that they have included with MySQL.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License, version 2.0, for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301  USA

# 
# The MySQL  Server configuration file.
# 
# For explanations see
# http://dev.mysql.com/doc/mysql/en/server-system-variables.html

[mysqld]
"""


# client_args = {
#     "port": "3306",
#     "socket": "/data/3306/mysql.sock",   
#     }

# /etc/mysql/mysql.conf.d/mysqld.cnf
with codecs.open(r'mysqld.cnf', 'w', 'utf-8') as fp:
    fp.write(mysqld_info)
    for k0,v0 in mysqld_args.items():
        fp.write("{}={}\n".format(k0,str(v0)))