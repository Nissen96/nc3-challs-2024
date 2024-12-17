# Start container and add source and build scripts
FROM debian:12.4

RUN apt-get update
RUN apt-get install -y gcc

COPY interpret.c .
COPY compile.sh .

# Run build scripts
CMD "./compile.sh"
