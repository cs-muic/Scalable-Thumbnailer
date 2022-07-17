import os 
import sys 
import redis
from rq import Worker, Queue, Connection
from redisconn import *
from extractor import *
from composer import *

if __name__ == '__main__':
    r = redis.Redis(host='redis', port=6379)
    with Connection(r):
        worker0 = Worker(id_queue, connection=r)
        worker1 = Worker(ex_queue, connection=r)
        worker2 = Worker(comp_queue, connection=r)
        worker3 = Worker(work_queue, connection=r)
        worker0.work()
        worker1.work()
        worker2.work()
        worker3.work()
