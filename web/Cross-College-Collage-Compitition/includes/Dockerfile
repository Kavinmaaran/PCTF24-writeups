FROM python:3.9.18-alpine3.19


WORKDIR /application


ARG UID=1000
ARG GID=1000
ENV DONTRUNBYTECODE = true
RUN echo "http://dl-cdn.alpinelinux.org/alpine/edge/community" > /etc/apk/repositories
RUN echo "http://dl-cdn.alpinelinux.org/alpine/edge/main" >> /etc/apk/repositories
RUN apk update
RUN apk add --no-cache --virtual .build-deps g++ python3-dev libffi-dev openssl-dev pkgconfig bash chromium chromium-chromedriver gcc musl-dev curl libmagic zlib-dev libjpeg-turbo-dev xvfb libxml2-dev libxslt-dev python3-dev && \
    apk add --no-cache --update python3 && \
     pip3 install --upgrade pip setuptools \
    && addgroup -g "${GID}" flaskapp && adduser -S -G flaskapp -D -u "${UID}" flaskapp

RUN python3 -m pip install --upgrade pip
COPY requirements.txt .
RUN python3 -m pip install -r requirements.txt
COPY . .
RUN chown -R flaskapp:flaskapp /application
RUN chmod +x "start.sh"
USER flaskapp
EXPOSE 8000
ENTRYPOINT [ "/application/start.sh" ]