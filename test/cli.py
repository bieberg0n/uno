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


def main():
    serv_addr = ('127.0.0.1', 9900)
    cli = Client(serv_addr)
    cli.join()
    cli.recv()
    cli.ready()
    cli.push(cli.cards[0])

    # resp = json.loads(s.recv(512).decode())
    # log(resp)
    # cards = resp['cards']

    # msg = dict(
    #     action='push',
    #     id=data['id'],
    #     cards=[cards[0]]
    #     # cards=['y9']
    # )
    # s.sendall(json.dumps(msg).encode())
    # print(json.loads(s.recv(512).decode()))
    # print(json.loads(s.recv(512).decode()))


main()
