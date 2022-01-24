import socket
import json
from os import _exit
from threading import Thread
from time import sleep

# conf
HOST = "localhost"
PORT = 54789

GAME_TIME = 15
DESIRED_SCORE = 10000

# score
my_score = 0
opponent_score = 0


# define threads
class send_points(Thread):
    def __init__(self, conn):
        super().__init__()
        self.conn = conn

        self.delay = GAME_TIME / DESIRED_SCORE

    def run(self):
        global my_score
        while True:
            try:
                self.conn.send("1".encode("utf-8"))
                my_score += 1
                sleep(self.delay)
            except:
                pass

class timer(Thread):
    def __init__(self, s):
        super().__init__()
        self.s = s

    def run(self):
        sleep(self.s)
        
        # run on exit
        conn.close()
        print(f"Opponent score was {opponent_score}")
        _exit(0)


# init socket
server = socket.socket()
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# bind host and port
server.bind((HOST, PORT))

# start listening
server.listen()

# print convincing message
print("Waiting for opponent connection...")

# accept connections
conn, addr = server.accept()

# grab json header data from connection
header = json.loads(conn.recv(1024).decode("utf-8"))

# check valid auth in header
if header["auth"] != "gwXu={f>2%4U5/>d":
            conn.close()
            print("Bad client authentication")
            _exit(0)

# print convincing message again
print(f"\n[LSCLEAR] {addr[0]} connected")

# start timer thread
timer_th = timer(GAME_TIME)
timer_th.start()

# start thread for sending points
sender = send_points(conn)
sender.start()

# receive points from client
try:
    while True:
        msg = conn.recv(1024)
        if msg:
            if msg.decode("utf-8") == "1":
                opponent_score += 1
except ConnectionResetError:
    pass

