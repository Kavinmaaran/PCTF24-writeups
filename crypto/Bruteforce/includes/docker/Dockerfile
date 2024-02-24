FROM python:slim AS app
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

FROM pwn.red/jail
COPY --from=app / /srv
COPY key /srv/app/key
COPY script.py /srv/app/run
ENV JAIL_MEM=30M JAIL_TIME=0 JAIL_CPU=0