FROM ubuntu:18.04

COPY /webapp /app
WORKDIR /app

RUN mkdir frames
RUN mkdir gif
RUN mkdir video

ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8

RUN apt-get -y update 
RUN apt-get install -y python3 
RUN apt-get install -y python3-pip
RUN apt-get install -y ffmpeg    
RUN apt-get install -y imagemagick

COPY requirements.txt /app/requirements.txt

RUN pip3 install -r /app/requirements.txt

CMD ["gunicorn", "-b 0.0.0.0:5000", "-w 2", "app:app"]