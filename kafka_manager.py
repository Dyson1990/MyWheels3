# -*- coding: utf-8 -*-
"""
Created on Wed Mar 22 16:43:51 2023

@author: Weave
"""
import sys
from pathlib import Path
py_dir = Path(__file__).parent

import kafka
import contextlib
import json

from loguru import logger

class KafkaConn():
    
    def __init__(self, topic, group, host="192.168.1.202", port="9092", partition=0):
        self.topic = topic
        self.group = group
        self.partition = partition
        
        self.producer = kafka.KafkaProducer(
            bootstrap_servers=[f'{host}:{port}'] 
            , key_serializer=lambda k: json.dumps(k).encode('utf-8')
            , value_serializer=lambda v: json.dumps(v).encode('utf-8')
            , api_version=(0,10,0)
        )
        
        self.consumer = kafka.KafkaConsumer(
            topic
            , bootstrap_servers=f'{host}:{port}'
            , group_id=group
        )
        
    def put_one(self, k0, v0):
        # help(self.producer.send)
        resp = self.producer.send(
            self.topic,
            # {k0: v0}
            key=k0,  # 同一个key值，会被送至同一个分区
            value=v0,
            # partition=self.partition
            )  # 向分区0发送消息
        logger.info(f"sending {v0}")
        try:
            resp.get(timeout=10) # 监控是否发送成功           
        except kafka.errors.KafkaTimeoutError as e0:  # 发送失败抛出kafka_errors
            logger.exception(e0)
    # def put(self, k0, v_list):
    #     for v0 in v_list:

    
    def get(self):
        for message in self.consumer:
            logger.info("receive, key: {}, value: {}".format(
                json.loads(message.key.decode()),
                json.loads(message.value.decode())
                )
            )
    
if __name__ == "__main__":
    obj = KafkaConn("test", "213")
    obj.put_one("k0", "34565645")
    
    # obj.get()