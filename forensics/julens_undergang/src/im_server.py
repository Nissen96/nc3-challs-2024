import json
import os
import pwn
import random
import sys
import time

pwn.context.log_level = "warn"


def chat(conn):
    with open("static/chat.json") as f:
        messages = json.load(f)
    os.remove("static/chat.json")

    if not conn.recvline().strip() == b"#START CHAT#":
        return
    
    conn.sendline(b"#CHAT ACCEPTED#")
    for from_client, msg in messages:
        if from_client:
            response = conn.recvline().strip()
            if response == b"#END CHAT#":
                conn.sendline(b"#CHAT ENDED#")
                return
        else:
            time.sleep(random.randint(len(msg) // 10, len(msg) // 5))
            conn.sendline(b"#MSG# " + msg.encode())

    if conn.recvline().strip() == b"#END CHAT#":
        conn.sendline(b"#CHAT ENDED#")
        conn.close()


def main():
    port = int(sys.argv[1])
    s = pwn.server(port, callback=chat, fam="ipv4")
    print("Waiting for connections...")
    while True:
        s.next_connection()


if __name__ == "__main__":
    main()
