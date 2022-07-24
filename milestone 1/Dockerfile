FROM ubuntu:18.04

WORKDIR /
COPY makethumbnail.py /

RUN mkdir video
RUN mkdir frames

RUN apt-get -y update
RUN apt-get install -y ffmpeg
RUN apt-get install -y python3
RUN apt-get install -y imagemagick

ENTRYPOINT [ "python3", "./makethumbnail.py" ]