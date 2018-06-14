import * as net from 'net'
import * as uuid from 'node-uuid'
import Decker from './dealer'


const HOST = '127.0.0.1'
const PORT = 9900

const log = function <T>(...args: T[]) {
    console.log(...args)
}

class Player {
    conn: net.Socket
    id: string
    status: string
    cards: Set<string>

    constructor(conn: net.Socket, id: string, status: string, cards: Set<string>) {
        this.conn = conn
        this.id = id
        this.status = status
        this.cards = cards
    }

    // cardInCards(card: string): boolean {
    //     // const a = new Map(
    //     return this.cards.has(card)
    // }

    cardsInCards(cards: string[]): boolean {
        return cards.every(card => this.cards.has(card))
    }
}

class Message {
    action: string
    id: string
    msg: string
    cards: string[]

    constructor(action: string, id: string, msg: string, deckList: string[]) {
        this.action = action
        this.id = id
        this.msg = msg
        this.cards = deckList
    }
}

class UnoServer {
    status: string
    players: Map<string, Player>
    decker: Decker

    constructor() {
        this.status = 'lobby'
        this.players = new Map()
        this.decker = new Decker()
    }

    join(conn: net.Socket) {
        log(`${conn.remoteAddress}:${conn.remotePort} join`)
        const newId = uuid.v4()
        const player = new Player(conn, newId, 'join', new Set([]))
        this.players.set(newId, player)
        const m = new Message('', player.id, '', [])
        conn.write(JSON.stringify(m))
        this.broadcast(player.id.slice(0, 6) + ' join.')
    }

    ready(conn: net.Socket, msg: Message) {
        const player = this.players.get(msg.id)
        log(`${conn.remoteAddress}:${conn.remotePort} ${msg.id} ready`)
        if (player === undefined) {
            log('err player')
            return
        } else {
            player.status = msg.action
            for (let [_, p] of this.players) {
                if (p.status !== 'ready') {
                    return
                }
            }
            this.status = 'playing'
            log('playing')
            this.dealCards()
            this.pushCards()
        }
    }

    lobby(conn: net.Socket, msg: Message) {
        if ((msg.action === 'join') && !this.players.has(msg.id)) {
            this.join(conn)

        } else if ((msg.action === 'ready') && this.players.has(msg.id)) {
            this.ready(conn, msg)
        }
    }

    dealCards() {
        for (let [_, p] of this.players) {
            p.cards = new Set(this.decker.pops(5))
        }
    }

    pushCards() {
        for (let [_, p] of this.players) {
            const msg = new Message('', p.id, '', Array.from(p.cards))
            p.conn.write(JSON.stringify(msg))
        }
    }

    playingcheck(player: Player, msg: Message): boolean {
        // if (!this.players.has(msg.id)) {
        //     log('players not have id')
        //     return false

        // } else
        if (msg.action === 'push') {
            // const player = this.players.get(msg.id)
            if (msg.cards.length !== 1 ||
                !player.cards.has(msg.cards[0])
            ) {
                log('no player or len to long or not have card')
                return false
            }
        }

        return true
    }

    syncCards(player: Player) {
        const msg = new Message('', player.id, '', Array.from(player.cards))
        player.conn.write(JSON.stringify(msg))
    }

    playing(conn: net.Socket, msg: Message) {
        const player = this.players.get(msg.id)
        if (player === undefined) {
            return

        } else if (!this.playingcheck(player, msg)) {
            return
        }

        player.conn = conn
        if (msg.action === 'push') {
            player.cards.delete(msg.cards[0])
            this.syncCards(player)
            this.broadcast(`${player.id.slice(0, 6)} push ${msg.cards[0]}`)

        } else {
            log('inv msg')
        }
    }

    broadcast(msgStr: string) {
        const message = new Message('', 'b', msgStr, [])
        for (let [_, p] of this.players) {
            try {
                p.conn.write(JSON.stringify(message))
            } catch(e) {
                log(e)
            }
        }
    }

    handle(conn: net.Socket, data: string) {
        const msg: Message = JSON.parse(data)
        log(`${conn.remoteAddress}:${conn.remotePort} action: ${msg.action}`)
        if (this.status === 'lobby') {
            this.lobby(conn, msg)

        } else if (this.status === 'playing') {
            this.playing(conn, msg)
        }
    }
}

const unoServer = new UnoServer()

const handle = function (conn: net.Socket) {
    conn.on('data', function (data: string) {
        unoServer.handle(conn, data)
    })
    conn.on('CLOSED', function (data: string) {
        // unoServer.handle(conn, data)
    })
}

const main = function () {
    const serv = net.createServer(handle)
    serv.listen(PORT, HOST)
    log('Server listening on ' + HOST + ':' + PORT)
}

main()
// log('test')
// const a = new Set()