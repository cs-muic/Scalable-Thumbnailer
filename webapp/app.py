import redis
import json

from flask import Flask,redirect,render_template
from rq import Queue
from minio import Minio
from extractor import extraction
from redisconn import ex_queue,setkeyval,getval,id_queue,r
from miniocon import client

app = Flask(__name__)



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
    return render_template("control.html", inputs = allvidsname)

#Api that return the list of all gifs that is present in the bucket gifs of minio
@app.route('/allgifs', methods=['POST', 'GET'])
def allgifs():
    allgifsname = []
    gifs = client.list_objects("gifs", recursive=True)
    for gif in gifs:
        name = gif.object_name
        allgifsname.append(name)
    return render_template("display.html", bucket = "gifs", inputs = allgifsname)

#API that deletes a particular gif
@app.route("/delete/<gif>", methods = ['POST'])
def delete(gif):
    client.remove_object("gif", gif)
    return redirect("http://localhost:80/allvideos")

#API that deletes all the gifs
@app.route("/deletegifs", methods = ['POST'])
def deletegifs():
    allgifs = client.list_objects("gif", recursive=True)
    for gif in allgifs:
        client.remove_object("gif", gif.object_name)
    return redirect("http://localhost:80/allmovies")

#API that submits a job to the queue(convet one video)
@app.route("/convert/<input>", methods = ['POST'])
def convert(input):
    name = input.split(".")
    output = name[0] + ".gif"

    id=int(getval("currentId"))
    id_queue.enqueue(setkeyval,"currentID",str(id+1))
    ex_queue.enqueue(setkeyval, id, "Start downloading video")
    ex_queue.enqueue(extraction, input, output, id)

    return f"The ID for your current task is  ({id})"

#API that submits multiple jobs to 
@app.route("/convertall", methods = ['POST'])
def convertall():
    videos = client.list_objects("video", recursive=True)
    idlist = []
    for video in videos:
        vidname=video.object_name
        name = vidname.split(".")
        output = name[0] + ".gif"
        id=int(getval("currentId"))
        id_queue.enqueue(setkeyval,"currentID",str(id+1))
        ex_queue.enqueue(setkeyval, id, "Start downloading video")
        ex_queue.enqueue(extraction, video, output, id)
        idlist.append(id)

    return f"The IDs for all your tasks is  ({idlist})"

@app.route('/')
def home():
    id_queue.enqueue(setkeyval,"currentId","0")
    
    if not client.bucket_exists("video"):
        client.make_bucket("video")

    if not client.bucket_exists("frames"):
        client.make_bucket("frames")
        
    if not client.bucket_exists("gif"):
        client.make_bucket("gif")
    
    return render_template("home.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)






