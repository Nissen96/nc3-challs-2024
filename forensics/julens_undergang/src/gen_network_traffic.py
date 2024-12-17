import http.client
import json
import os
import pwn
import random
import signal
import socket
import subprocess
import time

from email.message import EmailMessage
from tlslite import HTTPTLSConnection, HandshakeSettings, SMTP_TLS

pwn.context.log_level = "warn"

HTTP_PORT = 80
HTTPS_PORT = 443
SMTP_PORT = 25
IM_PORT = 1337

# Force TLS 1.2 with RSA key exchange to allow easy decryption in Wireshark
tls_settings = HandshakeSettings()
tls_settings.keyExchangeNames = ["rsa"]
tls_settings.maxVersion = (3, 3)


def start_servers():
    print("[*] Starting HTTP server...")
    http_server = subprocess.Popen(f"python -m http.server {HTTP_PORT}", cwd="static/web", shell=True, preexec_fn=os.setsid)
    print("[*] Starting HTTPS server...")
    https_server = subprocess.Popen(f"tls.py server -k ../../keys/key.pem -c ../../keys/cert.pem localhost:{HTTPS_PORT}", cwd="static/web", shell=True, preexec_fn=os.setsid)
    print("[*] Starting SMTP server...")
    smtp_server = subprocess.Popen(f"smtp4dev --hostname=localhost --smtpport={SMTP_PORT} --tlsmode=StartTls --tlscertificate=$(pwd)/keys/cert.pem --tlscertificateprivatekey=$(pwd)/keys/key.pkcs8", shell=True, preexec_fn=os.setsid)
    print("[*] Starting Instant Messaging server...")
    im_server = subprocess.Popen(f"python im_server.py {IM_PORT}", shell=True, preexec_fn=os.setsid)
    return http_server, https_server #, smtp_server, im_server



class Client:
    def __init__(self, name, email):
        self.name = name
        self.email = email

    def https_get(self, url):
        https_conn = HTTPTLSConnection("localhost", HTTPS_PORT, settings=tls_settings, ignoreAbruptClose=False)

        https_conn.request("GET", url)
        html = https_conn.getresponse().read()
        for img in html.split(b"<img src=\"")[1:]:
            time.sleep(0.5)
            https_conn.request("GET", img[:img.index(b"\"")].decode())
            https_conn.getresponse().read()

        https_conn.close()
    
    def http_get(self, url):
        http_conn = http.client.HTTPConnection("localhost", HTTP_PORT)

        http_conn.request("GET", url)
        html = http_conn.getresponse().read()
        for img in html.split(b"<img src=\"")[1:]:
            time.sleep(0.5)
            http_conn.request("GET", img[:img.index(b"\"")].decode())
            http_conn.getresponse().read()

        http_conn.close()
    
    def smtp_send(self, recipient, subject, body=None, body_file=None):
        smtp_conn = SMTP_TLS("localhost", SMTP_PORT)
        smtp_conn.starttls(settings=tls_settings)

        msg = EmailMessage()
        
        if body_file is not None:
            with open(body_file) as f:
                msg.set_content(f.read())
        else:
            msg.set_content(body)

        msg["Subject"] = subject
        msg["From"] = f"{self.name} <{self.email}>"
        msg["To"] = f"{recipient.name} <{recipient.email}>"
        
        smtp_conn.send_message(msg)

        smtp_conn.close()
    
    def instant_messaging(self, messages):
        with open("static/chat.json", "w") as f:
            json.dump(messages, f)

        conn = pwn.remote("localhost", IM_PORT, fam="ipv4")
        conn.sendline(b"#START CHAT#")
        if not conn.recvline().strip() == b"#CHAT ACCEPTED#":
            print("Chat not accepted")
            return
        
        for from_client, msg in messages:
            if from_client:
                time.sleep(random.randint(len(msg) // 10, len(msg) // 5))
                conn.sendline(f"#MSG# {msg}".encode())
                print(f"#MSG# {msg}")
            else:
                response = conn.recvline().strip()
                print(response.decode())
                if response == b"#END CHAT#":
                    conn.sendline(b"#CHAT ENDED#")
                    return

        conn.sendline(b"#END CHAT#")
        conn.recvline()
        conn.close()


def main():
    servers = start_servers()
    time.sleep(3)

    try:
        # Generate a few personas
        krynfsk = Client("Krynfsk", "krynfsk013@kaos.gnom")  # Leak gnom
        grompf = Client("Grompf", "support@kaos.gnom")  # IT-support
        flomfq = Client("Flomfq", "flomfq@kaos.gnom")  # Tilfældig gnom
        qrorm = Client("Qrorm", "qrorm@kaos.gnom")  # Tilfældig gnom
        gnoklios = Client("Gnoklios", "ceo@kaos.gnom")  # CEO
        mailing_list = Client("Afdelingen for Julens Undergang", "undergang@kaos.gnom")

        # Random traffic, HTTPS, SMTP mail, and some unencryped HTTP by Krynfsk
        qrorm.https_get("index.html")
        time.sleep(10)
        flomfq.https_get("index.html")
        time.sleep(3)
        qrorm.https_get("nyheder.html")
        exit()
        time.sleep(137)
        qrorm.smtp_send(flomfq, "Weekend planer?", body_file="static/email/bio.eml")
        time.sleep(13)
        krynfsk.http_get("index.html")
        time.sleep(2)
        flomfq.https_get("plan.html")
        time.sleep(33)
        grompf.https_get("nyheder.html")
        time.sleep(123)
        grompf.https_get("wiki.html?q=hvorfor+er+vores+gnommedarbejdere+helt+uduelige")
        time.sleep(5)
        krynfsk.http_get("nisser.html")
        time.sleep(17)
        flomfq.https_get("nyheder.html")
        time.sleep(67)
        grompf.smtp_send(qrorm, "Ny computer og kode", body_file="static/email/ny_computer.eml")
        time.sleep(13)
        krynfsk.http_get("nyheder.html")
        time.sleep(5)
        qrorm.https_get("plan.html")
        time.sleep(27)
        krynfsk.http_get("wiki.html?q=hvordan+udpakker+man+en+zip+fil")
        time.sleep(12)
        krynfsk.http_get("wiki.html?q=hvordan+starter+jeg+tls+igen")
        time.sleep(23)
        krynfsk.http_get("wiki.html?q=hvordan+kontaktes+IT+support")
        time.sleep(138)

        # Krynfsk kontakter Qrorm på ukrypteret kanal for at få hjælp
        krynfsk.instant_messaging([
            (True, "Hallo, Krynfsk her, er der nogen fra IT-support?"),
            (False, "Ja mig, Grompf"),
            (False, "Det her er en gammel ukrypteret kanal, den må du slet ikke bruge, alt skal være krypteret nu!"),
            (True, "Ehhm, jeg har muligvis ved en fejl slået TLS fra og ved ikke, hvordan jeg får sat det op igen"),
            (False, "Jeg bliver så træt..."),
            (False, "Nå, men det burde være hurtigt at fikse, vi bruger samme RSA-nøgle til alt og alle i Kaos A/S, det var nemmest"),
            (True, "Nåååårh, ja jeg faldt godt over en private key i din rodekasse på fællesdrevet, det må være den!"),
            (False, "Ehhh, den troede jeg, jeg havde slettet igen... Det gør jeg lige med det samme..."),
            (True, "Bare rolig, hvis du mister den, kan vi altid genskabe den!"),
            (False, "Øhhhh hvad?!?"),
            (True, "Ja ja! Flomfq hjalp mig med at uploade primtallene til en online faktor database, så vi altid kan slå dem op igen ud fra public key!"),
            (False, "Det er simpelthen løgn, hvis en nisse får fat i den, er vi færdige hele bundtet..."),
            (True, "Skal jeg lige sende den, så du kan tjekke, om det er den rigtige?"),
            (False, "NEJ NEJ NEJ, du må endelig ikke sende den til nogen og ISÆR ikke over en ukrypteret kanal!"),
            (False, "Den private nøgle bruges af serveren til at opsætte TLS sessions - enhver der har den kan dekryptere ALT!"),
            (True, "Nå nå, ingen grund til at blive sur... Jeg kommer bare forbi dit kontor i stedet"),
        ])
        time.sleep(33)

        # He gets encryption up and running and all remaining traffic is encrypted
        krynfsk.https_get("index.html")
        time.sleep(7)
        krynfsk.https_get("wiki.html?q=hvad+betyder+tls+egentlig")
        time.sleep(117)
        krynfsk.smtp_send(grompf, "Tak!", body_file="static/email/tak.eml")
        time.sleep(7)
        krynfsk.https_get("plan.html")
        time.sleep(87)
        gnoklios.smtp_send(mailing_list, "Operation Julens Undergang", body_file="static/email/plan.eml")
        time.sleep(13)
        krynfsk.https_get("flag.html")
        
    except Exception as e:
        print(e)
    finally:
        print("[*] Closing servers...")
        time.sleep(2)
        for server in servers:
            os.killpg(os.getpgid(server.pid), signal.SIGTERM)
            time.sleep(1)


if __name__ == "__main__":
    main()
