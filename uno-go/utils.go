package main

import (
	"fmt"
	"net"
	"strings"
	"strconv"
)

func check(err error) {
	if err != nil {
		panic(err)
	}
}

func logs(args... interface{}) {
	fmt.Println(args...)
}

func makeUDPAddr(addr string) *net.UDPAddr {
	sp := strings.Split(addr, ":")
	port, _ := strconv.Atoi(sp[1])
	return &net.UDPAddr{
		IP: net.ParseIP(sp[0]),
		Port: port,
	}
}