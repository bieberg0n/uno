from uno import Table


def test_next_can_do():
    table = Table()
    table.add_player('aa')
    table.add_player('bb')

    aa = table.players['aa']

    assert table.can_do == 0
    aa.lead(aa.cards[0])
    assert table.can_do == 1


def test_win():
    table = Table()
    table.add_player('aa')
    table.add_player('bb')

    aa = table.players['aa']
    aa.cards = ['红1']
    aa.lead(aa.cards[0])
    assert len(table.players.keys()) == 0


if __name__ == '__main__':
    test_next_can_do()
    test_win()