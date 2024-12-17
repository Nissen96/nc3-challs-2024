FROM python:3.12

COPY src /app
WORKDIR /app

RUN apt-get update
RUN apt-get install -y socat

RUN pip install --upgrade pip
RUN pip install pycryptodome

EXPOSE 1337

ENTRYPOINT ["socat", "TCP-LISTEN:1337,fork,reuseaddr,bind=0.0.0.0", "EXEC:'python postnordpolen-1.py'"]
