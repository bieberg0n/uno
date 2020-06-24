import random
from utils import log


class Card:
    def __init__(self, color='红', value='0', type=''):
        self.color = color
        self.value = value
        self.type = type
        self.choose_color = ''

    @classmethod
    def generate_cards(cls):
        colors = ['红', '黄', '绿', '蓝']
        # 暂时没有 '跳过'
        values = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

        # generate a complete cards
        cards = [Card(color=n, value=m) for n in colors for m in values for _ in range(2)] + \
                [Card(color=c, value='2', type='add') for c in colors for _ in range(4)] + \
                [Card(color=c, value='反转', type='reverse') for c in colors for _ in range(4)] + \
                [Card(color='黑', value='4', type='add') for _ in range(8)] + \
                [Card(color='黑', value='转色') for _ in range(8)]

        random.shuffle(cards)
        return cards

    def to_str(self):
        color = self.color

        add_s = ''
        if self.type == 'add':
            add_s = '+'

        s = color + add_s + self.value
        return s

    def __str__(self):
        return self.to_str()

    @classmethod
    def load(cls, s):
        card = Card()
        card.color = s[0]

        if len(s) == 4:
            card.choose_color = s[3]

        if s[1] == '+':
            card.type = 'add'
            card.value = s[2]
        else:
            if s[1] == '反':
                card.type = 'reverse'
            card.value = s[1:3]

        return card

    @classmethod
    def cards_to_str(cls, cards):
        return [c.to_str() for c in cards]

    @classmethod
    def delete(cls, cards, card):
        cards_str = [c.to_str() for c in cards]
        i = cards_str.index(card.to_str())

        new_cards = cards[:i] + cards[i+1:]
        return new_cards

    @classmethod
    def include(cls, cards, card):
        # log(card.to_str(), list((c.to_str() for c in cards)))
        return card.to_str() in (c.to_str() for c in cards)


if __name__ == '__main__':
    for card in Card.generate_cards():
        log(card)
