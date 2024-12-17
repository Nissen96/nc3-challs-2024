FROM debian:12.4

RUN apt-get update
RUN apt-get install -y socat

RUN useradd -d /home/ctf/ -m -p ctf -s /bin/bash ctf
RUN echo "ctf:ctf" | chpasswd

WORKDIR /home/ctf

COPY nisseby-2 .
COPY flag.txt .

RUN chown -R root:root /home/ctf

USER ctf
EXPOSE 1337
CMD ["socat", "TCP-LISTEN:1337,reuseaddr,fork", "EXEC:./nisseby-2"]
