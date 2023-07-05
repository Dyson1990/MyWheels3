# -*- coding: utf-8 -*-
"""
Created on Tue Jun 20 17:24:03 2023

@author: Weave
"""

from pathlib import Path
from pyperf import Runner
from faker import Faker
import importlib.util

# 暂时不能用

# def run_text(my_function, inputs, report_p=Path("benchmark_results.json")):
#     # 创建基准测试 runner 实例
#     runner = Runner()
    
#     for name, input_data in inputs:
#         def test_func():
#             my_function(input_data)
    
#         runner.bench_func(name, test_func)
    
#     # 运行基准测试并生成报告
#     results = runner.run()
    
#     # 将测试结果保存到 JSON 文件中
#     with open(report_p, "w") as f:
#         results.dump(f)
    
#     # 在控制台中打印测试报告
#     results.display(show_metadata=True)

def faker_data(nrows=100):
    fake = Faker('zh_CN')

    for _ in range(nrows):
        yield {
            'name': fake.name(),
            'address': fake.address(),
            'email': fake.email(),
            'phone_number': fake.phone_number(),
            'date_time': fake.date_time(),
            'integer': fake.random_int(),
            'float_num': fake.pyfloat(),
            'text': fake.text(),
            'boolean': fake.boolean(),
            'url': fake.url()
        }
        
def insert_update_test(d_fields, d_rows):
    import pymysql
    from functools import reduce
    # 连接 MySQL 数据库
    conn = pymysql.connect(
        host='192.168.1.23',  # 数据库地址
        user='root',       # 数据库用户名
        password='*ycy123*', # 数据库密码
        database='tmp'  # 数据库名称
    )
    
    # 创建游标对象
    cur = conn.cursor()
    
    # 建表语句
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS fake_data (
      `id` INT NOT NULL AUTO_INCREMENT,
      `name` VARCHAR(255) NOT NULL,
      `address` VARCHAR(255) NOT NULL,
      `email` VARCHAR(255) NOT NULL,
      `phone_number` VARCHAR(20) NOT NULL,
      `date_time` DATETIME NOT NULL,
      `integer` INT NOT NULL,
      `float_num` FLOAT(6, 2) NOT NULL,
      `text` TEXT NOT NULL,
      `boolean` BOOLEAN NOT NULL,
      `url` VARCHAR(255) NOT NULL,
      PRIMARY KEY (id)
    );
    """
    
    # 执行建表操作
    cur.execute(create_table_sql)
    
    # 插入假数据到 MySQL 数据库中
    blanks = ",".join(["(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)" * len(d_rows)])
    d_fields = [f"`{s0}`" for s0 in d_fields]
    sql = f'INSERT INTO fake_data ({",".join(d_fields)}) VALUES {blanks}'
    val = tuple(reduce(lambda l1, l2: l1 + l2, d_rows))
    cur.execute(sql, val)
    conn.commit()
    
    # 关闭游标和数据库连接
    cur.close()
    conn.close()

if __name__ == "__main__":
    # spec = importlib.util.spec_from_file_location("my_module", "/path/to/my_module.py")
    # my_module = importlib.util.module_from_spec(spec)
    # spec.loader.exec_module(my_module)
    
    # 创建基准测试 runner 实例
    runner = Runner()
    
    for nrows in range(1000, 20000, 3000):
        nrows = nrows + 1
        data_gen = faker_data(nrows)
        
        fields = next(data_gen).keys()
        rows = [d0.items() for d0 in data_gen]
        
        def test_func():
            insert_update_test(fields, rows)
        
        runner.bench_func(f"nrows[{nrows-1}]", test_func)

        
    # 运行基准测试并生成报告
    results = runner.run()
        
    # 将测试结果保存到 JSON 文件中
    with open(Path("benchmark_results.json"), "w") as f:
        results.dump(f)
    
    # 在控制台中打印测试报告
    results.display(show_metadata=True)
    
    
# =============================================================================
# import pyperf
# import pymysql
# 
# # 连接 MySQL 数据库
# conn = pymysql.connect(
#     host='localhost',
#     port=3306,
#     user='root',
#     password='your_password_here',
#     db='test_db'
# )
# 
# # 获取存储在 Python 列表中的数据
# def get_data(num_rows):
#     data = [[i, f'value-{i}'] for i in range(num_rows)]
#     return data
# 
# def insert_batch(data, batch_size):
#     with conn.cursor() as cursor:
#         for i in range(0, len(data), batch_size):
#             batch = data[i:i+batch_size]
#             sql = "INSERT INTO test_table (id, value) VALUES (%s, %s)"
#             cursor.executemany(sql, batch)
#         conn.commit()
# 
# # 设置不同的批大小值进行测试
# batch_sizes = [10, 20, 50, 100, 200, 500]
# 
# # 获取范围内的测试数据量
# num_rows = 1000000
# 
# # 生成测试集
# data = get_data(num_rows)
# 
# runner = pyperf.Runner()
# 
# # 微基准测试 - 对每个批量大小进行测试，并记录每次测试的平均时间
# results = {}
# for batch_size in batch_sizes:
#     def test_insert_batch():
#         insert_batch(data, batch_size)
# 
#     result = runner.timeit(
#         name='batch_size_{}'.format(batch_size),
#         func=test_insert_batch,
#         inner_loops=1
#     )
#     results[batch_size] = num_rows / result.median
# 
# # 查找最优批大小值：最大化每秒插入的数据量
# best_batch_size = max(results, key=results.get)
# 
# print(f"在 {num_rows} 条数据中，每次插入 {best_batch_size} 条数据效率最高，每秒插入 {results[best_batch_size]:.02f} 条数据")
# 
# # 将基准测试结果保存到 SQLite 数据库中
# runner.save('insert_benchmark_results.json')
# 
# # 生成 HTML 格式的测试报告
# pyperf.show('insert_benchmark_results.json', 'insert_report.html')
# =============================================================================

