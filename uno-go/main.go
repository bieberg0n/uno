package main

import "net"

const (
	IP = "127.0.0.1"
	Port = 9900
)

type UNOServer struct {
	conn *net.UDPConn
	players map[string] string
}

func NewUNOServer () *UNOServer {
	serv := new(UNOServer)
	serv.players = make(map[string] string)
	return serv
}

func (serv *UNOServer) broadcast(msg string) {
	for addr, _ := range serv.players {
		serv.conn.WriteToUDP([]byte(msg), makeUDPAddr(addr))
	}
}

func (serv *UNOServer) handle(msg string, addr string) {
	// TODO 大厅/游戏中 权限控制

	action := string(msg[0])
	data := string(msg[1:])

	if action == "j" {
		username := data
		logs(username, "join")
		serv.players[addr] = username

	} else if action == "s" {
		m := serv.players[addr] + "say: " + data
		logs(m)
		serv.broadcast(m)

	} else if action == "g" && serv.players[addr] == "bj" {
		logs("go")

	}
}

func (serv *UNOServer) Start() {
	conn, err := net.ListenUDP("udp", &net.UDPAddr{IP: net.ParseIP(IP), Port: Port})
	check(err)
	serv.conn = conn
	logs("server start on", IP, Port)

	data := make([]byte, 2048)
	for {
		n, addr, err := conn.ReadFromUDP(data)
		check(err)

		msg := string(data[:n])
		logs(addr, msg)
		serv.handle(msg, addr.String())
	}
}

func main() {
	serv := NewUNOServer()
	serv.Start()
}