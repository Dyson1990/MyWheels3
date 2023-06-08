# -*- coding: utf-8 -*-
"""
Created on Wed Jun  7 17:20:42 2023

@author: Weave
"""

class Base:
    
    def __init__(self):
        self.meta = []
        self.data = []
    
    def get(self):
        return self.meta, self.data
    
    def put(self, row):
        self.data.append(row)
    
class MinSize(Base):
    
    def __init__(self):
        self.meta = bytearray()
        self.data = bytearray()
        
    def __to_bytes(obj):
        pass
        
    def get(self):
        return self.meta, self.data
        
    def put(self, row):
        self.data.append(row)
        
if __name__ == "__main__":
    data = MinSize()
    
    