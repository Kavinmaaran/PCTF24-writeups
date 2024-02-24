FROM debian:buster-slim  AS build
RUN apt-get update && \
    apt-get install --no-install-suggests --no-install-recommends --yes build-essential libpq-dev python3-venv gcc libpython3-dev coreutils netcat && \
    python3 -m venv /venv && \
    /venv/bin/pip install --upgrade pip setuptools wheel

RUN adduser ICanDoThisAllDay --force-badname
RUN useradd -M -d /pickle pickle
RUN echo pickle:regex | chpasswd

RUN mkdir -p /pickle/security/is/compromised
RUN mkdir -p /pickle/ctf/is/very/fun
RUN mkdir -p /pickle/ctf/is/not/fun
RUN mkdir -p /pickle/module/is/dangerously/fun

RUN echo p_ctf{p1cKle_Is_v3ry_bAd} > /pickle/ctf/is/very/fun/flag.txt
RUN chown pickle:pickle /pickle/ctf/is/very/fun/flag.txt
RUN chmod 400 /pickle/ctf/is/very/fun/flag.txt

# Build the virtualenv as a separate step: Only re-execute this step when requirements.txt changes
FROM build AS build-venv
COPY requirements.txt /requirements.txt
RUN /venv/bin/pip install --disable-pip-version-check -r /requirements.txt

FROM busybox:1.35.0-uclibc as busybox

# Copy the virtualenv into a distroless image
FROM gcr.io/distroless/python3-debian10
COPY --from=build-venv /venv /venv
COPY --from=build /etc/passwd /etc/passwd
COPY --from=build /etc/group /etc/group
COPY --from=build /etc/shadow /etc/shadow
COPY --from=build /bin/nc /bin/nc
COPY --from=busybox /bin/sh /bin/sh
COPY --from=busybox /bin/ls /bin/ls
COPY --from=busybox /bin/cat /bin/cat
COPY --from=busybox /bin/su /bin/su
COPY --from=ghcr.io/tarampampam/curl:8.6.0 /bin/curl /bin/curl
COPY --from=busybox /bin/ping /bin/ping
COPY --from=busybox /bin/wget /bin/wget
COPY --from=busybox /bin/chmod /bin/chmod
COPY --from=busybox /bin/whoami /bin/whoami
COPY --from=build /pickle /pickle  

COPY libselinux.so.1 /lib/libselinux.so.1
RUN chmod u+s /bin/su


COPY --from=build /usr/bin/mkfifo /bin/mkfifo

COPY . /app
WORKDIR /app
USER ICanDoThisAllDay

ENTRYPOINT ["/venv/bin/gunicorn", "-b", "0.0.0.0:5000", "app:app", "-w", "10"]

