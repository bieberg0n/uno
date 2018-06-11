import net = require('net')
import uuid = require('node-uuid')

const HOST = '127.0.0.1'
const PORT = 9900

const log = function<T>(...args: T[]) {
    console.log(...args)
}

class Player {
    conn: net.Socket
    id: string
    status: string

    constructor(conn: net.Socket, id: string, status: string) {
        this.conn = conn
        this.id = id
        this.status = status
    }
}

class Message {
    action: string
    id: string
    data: string[]

    constructor(action: string, id: string, data: string[]) {
        this.action = action
        this.id = id
        this.data = data
    }
}

class UnoServer {
    status: string
    players: Player[]

    constructor() {
        this.status = 'lobby'
        this.players = []
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
            const player = new Player(conn, uuid.v4(), 'join')
            this.players.push(player)
            conn.write(JSON.stringify(new Message('', player.id, [''])))

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
        }
    }

    handle(conn: net.Socket, data: string) {
        const msg: Message = JSON.parse(data)
        log(`${conn.remoteAddress}:${conn.remotePort} action: ${msg.action}`)
        // log(`mode: ${this.status}`)
        if (this.status === 'lobby') {
            // log('mode: lobby')
            this.lobby(msg, conn)
        }
        // })
    }
}

const unoServer = new UnoServer()

const handle = function(conn: net.Socket) {
    conn.on('data', function(data: string) {
        unoServer.handle(conn, data)
    })
}

const main = function() {
    // const handler = new Handler()
    const serv = net.createServer(handle)
    serv.listen(PORT, HOST)
    log('Server listening on ' + HOST +':'+ PORT);
}

main()
