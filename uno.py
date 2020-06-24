# _*_ encoding: utf-8 _*_

# This .py file is a server for a UNO game.

# import random
import time
import player
from card import Card
from utils import log
from config import debug, debug_card


class Table:
    def __init__(self, app):
        self.app = app
        self.cards = Card.generate_cards()
        self.players = {}
        self.can_do = 0
        self.last_card = None
        self.add_num = 0
        self.next_num = 1

    def player_total(self):
        return len(self.players.keys())

    def deliver_card(self):
        if len(self.cards) == 0:
            self.cards = Card.generate_cards()

        card_selected = self.cards.pop()
        return card_selected

    def deliver_cards(self, n):
        return [self.deliver_card() for _ in range(n)]

    def add_player(self, name, is_ai=False):
        if self.players.get(name):
            return

        if debug:
            cards = [Card.load(c) for c in debug_card[:]]
        else:
            cards = self.deliver_cards(5)
        p = player.Player(name, cards, self, is_ai)
        self.players[name] = p

    def next_can_do(self):
        n = self.can_do + self.next_num
        if n >= self.player_total():
            self.can_do = 0
        elif n < 0:
            self.can_do = self.player_total() - 1
        else:
            self.can_do = n

    def can_do_player_name(self):
        return list(self.players.keys())[self.can_do]

    def win(self):
        self.players = {}
        self.can_do = 0
        self.last_card = None

    def check_ai(self):
        p = self.players[self.can_do_player_name()]
        if p.is_ai:
            log(p.name, 'ai auto op')
            self.app.socketio.sleep(0.5)
            p.auto_op()
