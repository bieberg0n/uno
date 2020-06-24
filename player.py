from card import Card
from utils import log


class Player:
    def __init__(self, name, cards, table, is_ai=False):
        self.name = name
        self.cards = cards
        self.table = table
        self.is_ai = is_ai

    def draw(self):
        # 到我出牌了吗
        if self.table.can_do_player_name() != self.name:
            return False

        if self.table.add_num > 0:
            cards = self.table.deliver_cards(self.table.add_num)
            self.cards.extend(cards)
            self.table.add_num = 0
        else:
            self.cards.append(self.table.deliver_card())
        self.table.next_can_do()
        return True

    def lead_check(self, card):
        last_card = self.table.last_card

        # 到我出牌了吗
        if self.table.can_do_player_name() != self.name:
            log(1)
            return False

        elif not Card.include(self.cards, card):
            log(2)
            return False

        # # 最后一张不能是功能牌
        # elif len(self.cards) == 1 and card[1] not in str_numbers:
        #     return False

        # 开始+时不能出普通牌
        elif self.table.add_num > 0 and card.type != 'add' and card.value != '反转':
            log(3)
            return False

        elif last_card is None:
            return True
        elif card.color == '黑':
            return True
        elif card.color == last_card.color:
            return True
        elif card.value == last_card.value:
            return True
        elif self.table.add_num > 0 and card.type == 'add':
            return True
        # 跟上一张牌相近吗
        # elif (last_card is not None) and card.color != '黑' and card.color != last_card.color and card.type != last_card.type and (last_card.type == 'add' and card.type != 'reverse'):
        #     log(4)
        #     return False

        else:
            return False

    def lead(self, card):
        if not self.lead_check(card):
            log('check err')
            return False

        self.cards = Card.delete(self.cards, card)
        self.table.last_card = card
        if card.color == '黑':
            # self.cards.remove(card[:3])
            self.table.last_card.color = card.choose_color

        # else:
        #     self.cards = Card.delete(self.cards, card)
            # self.cards.remove(card)
            # self.table.last_card = card
        #     if card[1] == '反' and self.table.last_card[1] == '+':
        #         ...
        #     else:
        #         self.table.last_card = card

        # +
        if card.type == 'add':
            self.table.add_num += int(card.value)
        elif card.type == 'reverse':
            self.table.next_num *= -1

        # 赢?
        if len(self.cards) <= 0:
            str_numbers = (str(i) for i in range(10))
            # if card[1] in str_numbers:
            if card.type == '' and card.value in str_numbers:
                self.table.win()
                return True
            else:
                card = self.table.deliver_card()
                self.cards.append(card)

        self.table.next_can_do()
        return True

    def auto_op(self):
        cards_can_lead = [c for c in self.cards if self.lead_check(c)]

        if cards_can_lead:
            card = cards_can_lead[0]
            if card.color == '黑':
                card.choose_color = '红'

            self.table.app.lead(self, card)

        else:
            self.table.app.draw(self)
