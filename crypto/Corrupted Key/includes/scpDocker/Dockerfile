FROM alpine:3 as base
WORKDIR /home/alice
RUN apk add --update --no-cache openssh bash openrc
RUN rc-update add sshd
RUN adduser --system -s /bin/sh alice && echo "alice:mQg8cwWfsKIH0nRaeDADdr8H2CUst9jiJv1q9TXv" | chpasswd
RUN echo -e 'AllowUsers alice\nMatch User alice\n\tX11Forwarding no\n\tAllowTcpForwarding no\n\tPermitTTY no\n\nPasswordAuthentication no\nPermitRootLogin no' >> /etc/ssh/sshd_config && ssh-keygen -A
RUN chown -R root:root /home && mkdir -p .ssh
COPY ./authorized_keys ./.ssh/authorized_keys
RUN chown -R alice:nogroup .ssh && chmod 700 .ssh && chmod 600 .ssh/authorized_keys
COPY ./flag.txt ./
RUN chown alice:nogroup flag.txt && chmod 400 flag.txt

FROM gcr.io/distroless/static-debian12
COPY --from=base /etc/passwd /etc/passwd
COPY --from=base /etc/shadow /etc/shadow
COPY --from=base /etc/group /etc/group
COPY --from=base /home /home
COPY --from=base /bin/sh /bin/sh
COPY --from=base /usr/bin/scp /usr/bin/scp
COPY --from=base /usr/sbin/sshd /usr/sbin/sshd
COPY --from=base /etc/ssh /etc/ssh
COPY --from=base /lib/ld-musl-x86_64.so.1 /lib/ld-musl-x86_64.so.1
COPY --from=base /lib/libz.so.1 /lib/libz.so.1
COPY --from=base /lib/libcrypto.so.3 /lib/libcrypto.so.3
COPY --from=base /var/empty /var/empty

ENTRYPOINT [ "/usr/sbin/sshd", "-D" ]
