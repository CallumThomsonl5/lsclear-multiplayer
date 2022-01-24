# Author: Callum Thomson

from os import _exit
from threading import Thread
from time import sleep
import socket
import json

# conf
HOST = "192.168.0.70"
PORT = 54953
GAME_TIME = 15
AUTH = "gwXu={f>2%4U5/>d"

# threads
class timer_thread(Thread):
    def __init__(self, s):
        super().__init__()
        self.s = s

    def run(self):
        global game

        sleep(self.s)
        game.going = False

        print(f"\nYour opponents score was {server.opponent_score}")
        print(f"Your score was {game.score}")

        if server.opponent_score < game.score:
            print("You win!")
        elif server.opponent_score == game.score:
            print("Draw")
        else:
            print("You lose")

        _exit(0)

class game_thread(Thread):
    def __init__(self):
        super().__init__()
        self.score = 0
        self.going = True

    def run(self):
        ls = True
        while self.going:
            try:
                get_input = input("> ")
                if ls and get_input == "ls":
                    self.score += 1
                    server.send("1")
                    ls = False
                elif not ls and get_input == "clear":
                    self.score += 1
                    server.send("1")
                    ls = True
                elif get_input == "sd":
                    server.send("sd")
                else:
                    print("wrong")
            except ConnectionResetError:
                print("Connection ended before sending point")


class server_thread(Thread):
    def __init__(self, host, port, auth):
        super().__init__()
        self.server = socket.socket()
        self.server.bind((host, port))
        self.opponent_score = 0
        self.auth = auth
        self.client_ready = False

    def run(self):
        self.server.listen()
        print("Waiting for opponent...")

        self.conn, self.addr = self.server.accept()
        header = json.loads(self.conn.recv(1024).decode("utf-8"))

        if header["auth"] != self.auth:
            self.conn.close()
            print("Bad client authentication")
            _exit(0)

        print(f"\n[LSCLEAR] {self.addr[0]} connected")
        self.client_ready = True

        try:
            while True:
                msg = self.conn.recv(1024)
                if msg:
                    if msg.decode("utf-8") == "1":
                        self.opponent_score += 1
        except ConnectionResetError:
            pass

    def send(self, msg):
        self.conn.send(msg.encode("utf-8"))


server = server_thread(HOST, PORT, AUTH)
server.start()

game = game_thread()

while 1:
    if server.client_ready == True:
        game.start()
        timer_thread(GAME_TIME).start()
        break
