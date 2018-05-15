from f5.bigip import ManagementRoot
import certifi
import urllib3
import requests
import re
from  __builtin__ import any
from f5.utils.responses.handlers import Stats

from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
x_file = open('nodes.txt', 'r')
r=list()
s=list()
for i in x_file:
    i=i.split('\n',1)[0]
    r.append(i)
#print r
# Connect to the BigIP

mgmt = ManagementRoot("ip", "username", "pwd")
x_file=open('nodes.txt', 'r')


def get_pool_stats(p_name, p_partition):
    """Return all pool stats object (dict of dicts)"""
    pool = mgmt.tm.ltm.pools.pool.load(name=p_name, partition=p_partition)
    return pool.stats.load()

# Get a list of all pools on the BigIP and print their names and their
# members' names
#test=list()
pools = mgmt.tm.ltm.pools.get_collection()

##Below lines will print pool and pool members##

dict={}

#for pool in pools:
#     s=pool.name
#     print "Pool is:{} ".format(s)
#     for member in pool.members_s.get_collection():
#         t=member.name
#         print "members are: {}".format(t)

for pool in pools:
    test=list()
    t=list()
    u=list()
    for member in pool.members_s.get_collection():
          test.append((member.name).encode("utf-8"))
    for line in r:
        for i in test:
            if line in i:
               s.append((pool.name).encode("utf-8"))
               break
            else: continue
#print s
#sample=list()
for pool in pools:
    sample=list()
    man=list()
    for i in s:
        if pool.name not in i: continue
        else: 
            print pool.name
            for member in pool.members_s.get_collection():
                sample.append((member.name).encode("utf-8"))
                mbr_stats = Stats(member.stats.load())
#                print(mbr_stats.stat.status_availabilityState['description'])
                print member.name, "STATE: " ,mbr_stats.stat.status_availabilityState['description']
#                words = ["001","002"]
            if all('002' and '001' in i for i in sample): print "!!!NO REDUNDANT MEMBERS AVAILABLE!!!"'\n'
            else: print "***REDUNDANT MEMBERS AVAILABLE***"'\n'
