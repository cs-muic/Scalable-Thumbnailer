
import redis
import subprocess
import os

from redisconn import comp_queue,setkeyval
from composer import composing
from rq import Queue
from pathlib import Path
from minio import Minio

client = Minio(
        "host.docker.internal:9000",
        access_key="minio",
        secret_key="minio123",
        secure=False
    )

def extraction(input,output,id):
    vidpath = f'video/{id}/{input}'
    framepath=f'frames/{id}'
    if not(os.path.exists(vidpath)):
        Path(f'video/{id}').mkdir(parents=True,exist_ok=True)
        client.fget_object("video", input, vidpath)
        print("Successfully got the video")

    if not(os.path.exists(framepath)):
        Path(f'frames/{id}').mkdir(parents=True,exist_ok=True)
        
    cmd1=f'ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 video/{vidpath}'
    runcmd1= subprocess.run(cmd1, shell=True, stdout=subprocess.PIPE)
    time=float(runcmd1.stdout.decode('utf-8'))
    if (time<=60):
        temp=time*(1/3)
        extract_convert=f'ffmpeg -i "video/{vidpath}" -vf "select=not(mod(n\,10))" -vsync vfr -q:v 2 -ss {temp} -t {temp} "{framepath}/img_%04d.png"'
        subprocess.run(extract_convert, shell=True)
    else:
        temp=time*(2/3)
        extract_convert=f'ffmpeg -i "video/{vidpath}" -vf "select=not(mod(n\,10))" -vsync vfr -q:v 2 -ss {temp} -t 20 "{framepath}/img_%04d.png"'
        subprocess.run(extract_convert, shell=True)

    if not client.bucket_exists("frames"):
        client.make_bucket("frames")

    all=os.scandir(framepath)
    for file in all:
        if file.is_file()==True:
            client.fget_object("frames",f'{id}/{file.name}',file.path)

    comp_queue.enqueue(setkeyval,id,"Composing process has started")
    comp_queue.enqueue(composing,output,id)