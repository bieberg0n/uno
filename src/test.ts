import net = require('net')
const HOST = '127.0.0.1'
const PORT = 9900

function log<T>(...args: T[]) {
    console.log(...args)
}

function handle(conn: net.Socket) {
    console.log('CONNECTED: ' + conn.remoteAddress + ':' + conn.remotePort)
    conn.on('data', function(data: string) {
        console.log('DATA ' + conn.remoteAddress + ': ' + data)
        conn.write(data)
    })

    conn.on('close', function(data: string) {
        console.log('CLOSED: ' + conn.remoteAddress + ' ' + conn.remotePort)
    })

}

function main() {
    const serv = net.createServer(handle)
    serv.listen(PORT, HOST)
    console.log('Server listening on ' + HOST +':'+ PORT);
}

main()
