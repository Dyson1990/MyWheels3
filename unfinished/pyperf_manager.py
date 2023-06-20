# -*- coding: utf-8 -*-
"""
Created on Tue Jun 20 17:24:03 2023

@author: Weave
"""

from pyperf import Runner
from my_module import my_function

# 创建基准测试 runner 实例
runner = Runner()

# 定义一组不同大小的输入数据，并向 runner 注册测试函数
inputs = [
    ("small", [1, 2, 3]),
    ("medium", list(range(1000))),
    ("large", list(range(100000))),
]

for name, input_data in inputs:
    def test_func():
        my_function(input_data)

    runner.bench_func(name, test_func)

# 运行基准测试并生成报告
results = runner.run()

# 将测试结果保存到 JSON 文件中
with open("benchmark_results.json", "w") as f:
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

