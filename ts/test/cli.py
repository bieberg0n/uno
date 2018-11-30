import socket
import json


def log(*args):
    print(*args)


class Client:
    def __init__(self, serv_addr: tuple):
        self.conn = socket.socket()
        self.conn.connect(serv_addr)
        self.id = ''
        self.cards = list()

    def action(self, ac: str, cards: list = []):
        msg = dict(
            action=ac,
            id=self.id,
            cards=cards
        )
        self.conn.sendall(json.dumps(msg).encode())

    def recv(self):
        data_str = self.conn.recv(512).decode()
        data = json.loads(data_str)
        log(data)
        return data

    def join(self):
        self.action('join')
        data = self.recv()
        self.id = data['id']
        log(self.id)

    def ready(self):
        self.action('ready')
        data = self.recv()
        self.cards = data['cards']

    def push(self, card):
        self.action('push', [card])
        data = self.recv()
        self.cards = data['cards']

    def sync(self):
        self.action('cards')
        self.cards = self.recv()['cards']


def main():
    serv_addr = ('127.0.0.1', 9900)
    cli = Client(serv_addr)
    cli.join()
    cli.recv()
    cli.ready()

    while True:
        input_ = input(':').split(' ')
        op = input_[0]
        if op == 'push':
            card = input_[1]
            cli.push(card)
        elif op == 'show':
            cli.sync()
            log(cli.cards)


main()
