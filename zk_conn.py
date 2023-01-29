# -*- coding: utf-8 -*-
"""
Created on Wed Nov 30 14:21:31 2022

@author: Weave
"""
import sys
from pathlib import Path
py_dir = Path(__file__).parent

from kazoo.client import KazooClient
import re
import yaml
import hashlib

from loguru import logger


class ShardingRules:
    def __init__(self):
        self.zk = KazooClient(hosts='192.168.1.24:21810', use_ssl=False)
        self.zk.start()
        
        self.rules_path = "/governance/metadata/logic_db/versions/0/rules"
        rules_bytes = self.zk.get(self.rules_path)[0]
        self.org_table_md5 = hashlib.md5(rules_bytes).hexdigest()
        rules_str = rules_bytes.decode('utf-8')
        
        if rules_str.startswith("-"):
            rules_rows = rules_str.split("\n")
            self.rules_head = rules_rows[0]
            self.rules = yaml.load('\n'.join(rules_rows[1:]), yaml.Loader)
        else:
            self.rules_head = ""
            self.rules = rules_str
            
        self.key_generators = self.rules["keyGenerators"]
        self.sharding_algorithms = self.rules["shardingAlgorithms"]
        self.tables = self.rules["tables"]
        self.org_table_count = len(self.rules["tables"])
        
    def __del__(self):
        self.zk.stop()
        
    def rules_body(self):
        rules_body = re.sub(r"^", " "*2, yaml.dump(self.rules), flags=re.M)
        return rules_body
    
    def upload(self):
        content = self.rules_head+"\n"+self.rules_body()
        # print(content)
        md5 = hashlib.md5(content.encode("utf-8")).hexdigest()
        b1 = self.org_table_count == len(self.rules["tables"])
        b2 = self.org_table_md5 == md5
        # print("self.org_table_count", self.org_table_count)
        # print("len(self.rules[\"tables\"])", len(self.rules["tables"]))
        # print("self.org_table_md5", self.org_table_md5)
        # print("md5", md5)
        # print(b1, b2)
        if b1 and b2:
            # logger.warning("未发现有内容更新")
            raise Exception("未发现有内容更新，请检查新的rule对象是否有注册，或者节点修改不成功。")

        self.zk.set(self.rules_path, content.encode("utf-8"))
        logger.info("zookeeper更新成功")

class TableRule(ShardingRules):
    def __init__(self, logic_tn):
        super(TableRule,self).__init__()
        self.logic_tn = logic_tn
        if self.logic_tn in self.tables:
            self.rule = self.tables[self.logic_tn]
        else:
            self.rule = {'actualDataNodes': logic_tn
                         , 'tableStrategy': {'standard': {'shardingColumn': 'data_id'
                                                          , 'shardingAlgorithmName': 'boundary_range'
                                                          }
                                             }
                         }
        
    def set_data_nodes(self, cap, floor=0, db="sharding_db"):
        self.rule["actualDataNodes"] = f"{db}.{self.logic_tn}_S${{{floor}..{cap}}}"
        
    def register(self):
        self.tables[self.logic_tn] = self.rule
        

if __name__ == "__main__":
    # sharding_rules = ShardingRules()
    # sharding_rules.upload()
    for i0 in range(41, 62):
        t_rule = TableRule(f"ODS_DV{i0}")
        t_rule.set_data_nodes(20)
        t_rule.register()
        t_rule.upload()
        
        del t_rule
