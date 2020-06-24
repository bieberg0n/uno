#!/usr/bin/env python
from flask import Flask, send_file, redirect
from flask_socketio import SocketIO, emit
import uno
from card import Card
from config import port
from utils import (
log,
random_name,
)


class UnoServ:
    def __init__(self):
        app = Flask(__name__)
        app.config['SECRET_KEY'] = 'secret!'
        self.socketio = SocketIO(app, cors_allowed_origins='*')
        table = uno.Table(self)

        self.app = app
        self.table = table

    def lead(self, player, card):
        p = player
        name = p.name
        if not p.lead(card):
            return

        emit('broadcast', {
            'type': 'lead',
            'name': name,
            'card': card.to_str(),
            'remainCardsNum': len(p.cards)
        }, broadcast=True)

        if not p.is_ai:
            emit('push_cards', {'data': Card.cards_to_str(p.cards)})

        emit('broadcast', {
            # 'name': '轮到 {} 出牌'.format(table.can_do_player_name()),
            'name': table.can_do_player_name(),
            'type': 'next'
        }, broadcast=True)

        log(name, 'lead', card,  'finish', Card.cards_to_str(p.cards))
        uno_serv.table.check_ai()

    def draw(self, player):
        p = player
        name = p.name
        if not p.draw():
            return

        emit('broadcast', {
            'type': 'draw',
            'name': name,
            'remainCardsNum': len(p.cards)
        }, broadcast=True)

        if not player.is_ai:
            emit('push_cards', {'data': Card.cards_to_str(p.cards)})

        emit('broadcast', {
            # 'name': '轮到 {} 出牌'.format(table.can_do_player_name()),
            'name': self.table.can_do_player_name(),
            'type': 'next'
        }, broadcast=True)

        self.table.check_ai()


if __name__ == '__main__':
    uno_serv = UnoServ()
    app = uno_serv.app
    table = uno_serv.table
    socketio = uno_serv.socketio

    @app.route('/')
    def index():
        return send_file('index.html')


    @app.route('/restart')
    def restart():
        table.win()
        return redirect('/', 302)


    @app.route('/add_ai')
    def add_ai():
        # ai = Ai()
        table.add_player(random_name(), is_ai=True)
        return redirect('/', 302)


    @socketio.on('lead')
    def client_msg(msg):
        name = msg['name']
        card = Card.load(msg['card'])
        log(name, 'lead', card)

        p = table.players[name]
        uno_serv.lead(p, card)

    @socketio.on('draw')
    def client_msg(msg):
        name = msg['name']
        log(name, 'draw')

        p = table.players[name]
        uno_serv.draw(p)


    @socketio.on('say')
    def client_msg(msg):
        name = msg['name']
        log(name, 'say')

        emit('broadcast', {
            'type': 'say',
            'name': name,
            'say': msg['say'],
        }, broadcast=True)


    @socketio.on('connect_event')
    def connect(msg):
        name = msg['name']
        table.add_player(name)
        log(name, 'join in')

        emit('broadcast', {
            'type': 'join',
            'name': name,
            'players': list(table.players.keys())
        }, broadcast=True)

        # cards = [c.to_str() for c in table.players[name].cards]
        emit('push_cards', {'data': Card.cards_to_str(table.players[name].cards)})
        emit('broadcast', {
            # 'name': '轮到 {} 出牌'.format(table.can_do_player_name()),
            'name': table.can_do_player_name(),
            'type': 'next'
        }, broadcast=True)
        uno_serv.table.check_ai()


    log('listen on 0.0.0.0:', port, '...')
    socketio.run(app, host='0.0.0.0', port=port, debug=False)
