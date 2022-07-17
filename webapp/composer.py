import subprocess
import redis
import os

from redisconn import setkeyval,work_queue
from rq import Queue
from pathlib import Path
from minio import Minio
from miniocon import client

def composing(output,id):
    framepath = f'frames/{id}'
    gifpath = f"gif/{id}"
    if not(os.path.exists(framepath)):
        Path(framepath).mkdir(parents=True,exist_ok=True)
    if not(os.path.exists(gifpath)):
        Path(gifpath).mkdir(parents=True,exist_ok=True)

    allframes = client.list_objects("frames", recursive=True)
    for frame in allframes:
        client.fget_object("frames", frame.object_name, f"frames/{frame.object_name}")

    cmd = f"convert -resize 480x360 -delay 10 -loop 0 {framepath}/*.png {gifpath}/{output}"
    subprocess.run(cmd, shell=True)

    if not client.bucket_exists("gif"):
        client.make_bucket("gif")
    
    client.fput_object("gif", output, f'{gifpath}/{output}')

    work_queue.enqueue(setkeyval,id,"Compising process finished successfully")


    
    
    
    