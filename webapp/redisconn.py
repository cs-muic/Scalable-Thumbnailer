import redis
from rq import Queue

r = redis.Redis(host='redis', port=6379)

ex_queue=Queue(connection=r)
comp_queue=Queue(connection=r)
work_queue=Queue(connection=r)
id_queue=Queue(connection=r)

def setkeyval(key,val):
    r.set(key,val)

def getval(key):
    return r.get(key)

