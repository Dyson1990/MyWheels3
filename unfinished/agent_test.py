# -*- coding: utf-8 -*-
"""
Created on Wed Feb 22 13:59:53 2023

@author: Weave
"""


from twisted.internet import reactor
from twisted.web.client import Agent, readBody


def cbRequest(response):
    print(response)
    print(response.__dir__())
    print(response.version)
    print(response.code)
    print(response.phrase)
    d = readBody(response)
    d.addCallback(cbBody, "helloworld")
 
def cbBody(body,message):
    #print(body,message)
    pass
 
agent = Agent(reactor)
d = agent.request(b"GET",b"http://www.baidu.com",None,None)
d.addCallback(cbRequest)
reactor.run()