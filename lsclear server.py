# Author: Callum Thomson
# a

from os import _exit
from threading import Thread
from time import sleep
import socket
import json


class timer_thread(Thread):
    def __init__(self, seconds, callback):
        super().__init__()
        self.seconds = seconds
        self.callback = callback

    def timer(self):
        sleep(self.seconds)

    def run(self):
        self.timer()
        self.callback()


class main_program_thread(Thread):
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
                print("Connection ended before sending point")


class server_thread(Thread):
    def __init__(self, host, port):
        super().__init__()
        self.server = socket.socket()
        self.server.bind((host, port))
        self.opponent_score = 0
        self.started = False

    def run(self):
        self.server.listen()
        print("Waiting for opponent...")

        self.conn, self.addr = self.server.accept()
        header = json.loads(self.conn.recv(1024).decode("utf-8"))

        if header["auth"] != "gwXu={f>2%4U5/>d":
            self.conn.close()
            print("Bad client authentication")
            _exit(0)

        try:
            if header["name"] == "":
                self.opponent_name = "Player 2"
            else:
                self.opponent_name = header["name"]
        except KeyError:
            self.opponent_name = "Player 2"

        print(
            f"\n[Lsclear] {self.addr} {self.opponent_name} connected with headers: {header}")
        self.started = True

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


def end_game():
    main.going = False

    print(f"\nYour opponents score was {server.opponent_score}")
    print(f"Your score was {main.score}")

    if server.opponent_score < main.score:
        print("You win!")
    elif server.opponent_score == main.score:
        print("Draw")
    else:
        print("You lose")

    _exit(0)


server = server_thread("", 5000)
server.start()

main = main_program_thread()

while 1:
    if server.started == True:
        main.start()
        timer_thread(15, end_game).start()
        break
