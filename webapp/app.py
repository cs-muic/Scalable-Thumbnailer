import redis
import json

from flask import Flask,redirect
from rq import Queue
from minio import Minio
from extractor import extraction
from redisconn import ex_queue,setkeyval,getval

app = Flask(__name__)

client = Minio(
        "host.docker.internal:9000",
        access_key="minio",
        secret_key="minio123",
        secure=False
    )

#API that returns progress of a job
@app.route("/trackprogress/<id>", methods = ['POST'])
def trackprogress(id):
    try:
        value=getval(id)
        return value
    except:
        return "Id not found"

#Api that return the list of all vidoes that is present in the bucket video of minio
@app.route('/allvideos', methods=['POST', 'GET'])
def allvideos():
    allvidsname = []
    videos = client.list_objects("video", recursive=True)
    for video in videos:
        name = video.object_name
        allvidsname.append(name)
    return allvidsname

#Api that return the list of all gifs that is present in the bucket gifs of minio
@app.route('/allgifs', methods=['POST', 'GET'])
def allgifs():
    allgifsname = []
    gifs = client.list_objects("gifs", recursive=True)
    for gif in gifs:
        name = gif.object_name
        allgifsname.append(name)
    return allgifsname





