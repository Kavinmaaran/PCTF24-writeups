
FROM ubuntu:20.04

RUN apt-get update && \
    apt-get install -y python3 python3-pip


WORKDIR /app

COPY ./requirements.txt .

ENV DEBIAN_FRONTEND noninteractive

RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get install -y -q yelp
RUN apt-get install -y -q libxml-libxml-perl


COPY ./ .

EXPOSE 5000


CMD gunicorn -b :5000 app:app
