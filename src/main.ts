import net = require('net')
import uuid = require('node-uuid')
import Decker from './dealer'


const HOST = '127.0.0.1'
const PORT = 9900

const log = function<T>(...args: T[]) {
    console.log(...args)
}

class Player {
    conn: net.Socket
    id: string
    status: string
    cards: string[]

    constructor(conn: net.Socket, id: string, status: string, deckList: string[]) {
        this.conn = conn
        this.id = id
        this.status = status
        this.cards = deckList
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
    players: Player[]
    decker: Decker

    constructor() {
        this.status = 'lobby'
        this.players = []
        this.decker = new Decker()
    }

    idInPlayers(id: string): boolean {
        for (let player of this.players) {
            if (id === player.id) {
                return true
            }
        }
        return false
    }

    playerFromArr(id: string): Player {
        for (let player of this.players) {
            if (id === player.id) {
                return player
            }
        }
        return this.players[-1]
    }

    lobby(msg: Message, conn: net.Socket) {
        if ((msg.action === 'join') && !this.idInPlayers(msg.id)) {
            log(`${conn.remoteAddress}:${conn.remotePort} join`)
            const player = new Player(conn, uuid.v4(), 'join', [])
            this.players.push(player)
            const m = new Message('', player.id, '', [])
            conn.write(JSON.stringify(m))

       } else if ((msg.action === 'ready') && this.idInPlayers(msg.id)) {
            log(`${conn.remoteAddress}:${conn.remotePort} ready`)
            const player = this.playerFromArr(msg.id)
            player.status = msg.action
            for (let p of this.players) {
                if (p.status != 'ready') {
                    return
                }
            }
            this.status = 'playing'
            log('playing')
            this.dealCards()
            this.pushCards()
        }
    }

    dealCards() {
        for (let p of this.players) {
            p.cards = this.decker.pops(5)
        }
    }

    pushCards() {
        for (let p of this.players) {
            const msg = new Message('', p.id, '', p.cards)
            p.conn.write(JSON.stringify(msg))
        }
    }

    playing(msg: Message) {
        if (this.idInPlayers(msg.id)) {

        } else {
            return
        }
    }

    broadcast(msgStr: string) {
        const message = new Message('', 'b', msgStr, [])
        for (let p of this.players) {
            p.conn.write(JSON.stringify(message))
        }
    }

    handle(conn: net.Socket, data: string) {
        const msg: Message = JSON.parse(data)
        log(`${conn.remoteAddress}:${conn.remotePort} action: ${msg.action}`)
        if (this.status === 'lobby') {
            this.lobby(msg, conn)
        } else if (this.status === 'playing') {
            this.playing(msg)
        }
    }
}

const unoServer = new UnoServer()

const handle = function(conn: net.Socket) {
    conn.on('data', function(data: string) {
        unoServer.handle(conn, data)
    })
}

const main = function() {
    const serv = net.createServer(handle)
    serv.listen(PORT, HOST)
    log('Server listening on ' + HOST +':'+ PORT);
}

main()
// log('test')