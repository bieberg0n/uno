# _*_ encoding: utf-8 _*_

# This .py file is a server for a UNO game.

import random
from utils import log


def generate_cards():
    colors = ['红', '黄', '绿', '蓝']
    # 暂时没有反转牌   '跳过',
    symbols = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '+2', '反转']
    super_cards = ['黑转色', '黑+4']
    # generate a complete cards
    cards = [n + m for n in colors for m in symbols] * 2 + super_cards * 4
    return cards


class Table:
    def __init__(self):
        self.cards = generate_cards()
        self.players = {}
        self.can_do = 0
        self.last_card = ''
        self.add_num = 0
        self.next_num = 1

    def player_total(self):
        return len(self.players.keys())

    def deliver_card(self):
        if len(self.cards) == 0:
            self.cards = generate_cards()

        num = random.randint(0, len(self.cards) - 1)
        card_selected = self.cards.pop(num)
        return card_selected

    def deliver_cards(self, n):
        return [self.deliver_card() for _ in range(n)]

    def add_player(self, name):
        if self.players.get(name):
            return

        p = Player(name, self.deliver_cards(5), self)
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
        # for p in self.players.values():
        #     p.cards = self.deliver_cards(5)
        self.players = {}
        self.can_do = 0
        self.last_card = ''


class Player:
    def __init__(self, name, cards, table):
        self.name = name
        self.cards = cards
        self.table = table

    def draw(self):
        # 到我出牌了吗
        if self.table.can_do_player_name() != self.name:
            return False

        if self.table.add_num > 0:
            self.cards.extend(self.table.deliver_cards(self.table.add_num))
            self.table.add_num = 0
        else:
            self.cards.append(self.table.deliver_card())
        self.table.next_can_do()
        return True

    def lead_check(self, card):
        last_card = self.table.last_card
        # 到我出牌了吗
        if self.table.can_do_player_name() != self.name:
            return False

        # 开始+时不能出普通牌
        elif self.table.add_num > 0 and card[1] not in ('+', '反'):
            return False

        # 跟上一张牌相近吗
        elif last_card != '' and card[0] != '黑' and card[0] != last_card[0] and card[1:] != last_card[1:]:
            return False

        # 最后一张不能是功能牌
        elif len(self.cards) == 1 and card[1] not in (str(i) for i in range(10)):
            return False

        else:
            return True

    def lead(self, card):
        if not self.lead_check(card):
            return False

        if card[0] == '黑':
            log(self.cards)
            self.cards.remove(card[:3])
        else:
            self.cards.remove(card)

        # 赢
        if len(self.cards) <= 0:
            self.table.win()
            return True

        # 变色
        if card[0] == '黑':
            self.table.last_card = card[3] + card[1:2]
        else:
            self.table.last_card = card

        # +
        if card[1] == '+':
            self.table.add_num += int(card[2])
        elif card[1] == '反':
            self.table.next_num *= -1

        self.table.next_can_do()
        return True
