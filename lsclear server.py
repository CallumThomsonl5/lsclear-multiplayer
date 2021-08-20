# Author: Callum Thomson

from os import _exit
from threading import Thread
from time import sleep
import socket

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

    def run(self):
        ls = True
        while 1:
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
        print(f"\n{self.addr} connected")
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
    sleep(2)
    print(f"\nYour opponents score was {server.opponent_score}")
    print(f"Your score was {main.score}")

    if server.opponent_score < main.score:
        print("You win!")
    else:
        print("You lose")

    sleep(0.5)
    _exit(0)




server = server_thread("", 5000)
server.start()

main = main_program_thread()

while 1:
    if server.started == True:
        main.start()
        timer_thread(15, end_game).start()
        break