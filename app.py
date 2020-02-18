#!/usr/bin/env python
from flask import Flask, send_file
from flask_socketio import SocketIO, emit
from uno import Table
from config import port
from utils import log

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
table = Table()


@app.route('/')
def index():
    return send_file('index.html')


@socketio.on('lead')
def client_msg(msg):
    name = msg['name']
    card = msg['card']
    log(name, 'lead', card)

    p = table.players[name]
    if not p.lead(card):
        return

    emit('broadcast', {
        'type': 'lead',
        'name': name,
        'card': card,
        'remainCardsNum': len(p.cards)
    }, broadcast=True)
    emit('push_cards', {'data': p.cards})
    emit('broadcast', {
        # 'name': '轮到 {} 出牌'.format(table.can_do_player_name()),
        'name': table.can_do_player_name(),
        'type': 'next'
    }, broadcast=True)


@socketio.on('draw')
def client_msg(msg):
    name = msg['name']
    log(name, 'draw')

    p = table.players[name]
    if not p.draw():
        return

    emit('broadcast', {
        'type': 'draw',
        'name': name,
        'remainCardsNum': len(p.cards)
    }, broadcast=True)
    emit('push_cards', {'data': p.cards})
    emit('broadcast', {
        # 'name': '轮到 {} 出牌'.format(table.can_do_player_name()),
        'name': table.can_do_player_name(),
        'type': 'next'
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

    emit('push_cards', {'data': table.players[name].cards})


if __name__ == '__main__':
    # log('listen on 0.0.0.0:', port, '...')
    socketio.run(app, host='0.0.0.0', port=port, debug=True)
