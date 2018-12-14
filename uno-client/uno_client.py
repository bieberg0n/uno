import socket
from threading import Thread
from queue import Queue


def log(*args):
    print(*args)


class UNOClient:
    def __init__(self):
        self.host = ('127.0.0.1', 9900)
        self.name = input('你的名字:')
        self.s = socket.socket(2, 2)
        self.msg_history = Queue()
        Thread(target=self.print_recv).start()
        self.cards = []

        self.send('j' + self.name)
        self.get_some_card(5)
        # log(self.cards)
        self.play_loop()

    def print_recv(self):
        while True:
            msg_bytes, _ = self.s.recvfrom(512)
            msg = msg_bytes.decode()
            if msg.startswith(self.name):
                ...

            elif msg.startswith('p'):
                self.msg_history.put(msg[1:])

            else:
                log(msg)

    def send(self, msg):
        self.s.sendto(msg.encode(), self.host)

    def get_card(self):
        self.send('p')
        card = self.msg_history.get()
        self.cards.append(card)

    def get_some_card(self, n):
        for _ in range(n):
            self.get_card()

    def play(self):
        infies = ['出牌:']
        infies.extend([str(i) + '.' + card for i, card in enumerate(self.cards)])
        infies.append('p.摸牌')
        info = '[' + ' '.join(infies) + ']'
        log(info)
        op = input(':')
        if op in [str(i) for i in range(len(self.cards))]:
            index = int(op)
            card = self.cards[index]
            self.send('q' + card)
            log('出牌:', card)
            del self.cards[index]

            if len(self.cards) == 1:
                self.send('s'+ 'UNO!')

            elif op == 'p':
                self.get_card()

        else:
            log('错误的指令')

    def play_loop(self):
        while True:
            self.play()


def main():
    UNOClient()


main()
