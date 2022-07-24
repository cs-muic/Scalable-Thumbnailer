import os 
import sys 
import redis
from rq import Worker, Queue, Connection
from redisconn import *
from extractor import *
from composer import *

if __name__ == '__main__':
    with Connection(r):
        worker2 = Worker(comp_queue, connection=r)
        worker2.work()
