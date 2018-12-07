package main

import (
	"crypto/rand"
	"math/big"
	"strconv"
)

func Cards() []string {
	var cs []string
	var colors = []string{"红", "黄", "蓝", "绿"}
	for _, c := range colors {
		for i := 1; i <= 2; i++ {
			for i := 1; i <= 9; i++ {
				cs = append(cs, c+strconv.Itoa(i))
			}
		}
		cs = append(cs, c + "0")

		other := []string{
			"跳",
			"反",
			"+2",
		}
		for i:= 1; i <= 2; i++ {
			for _, o := range other {
				cs = append(cs, c+o)
			}
		}
	}

	for i := 1; i <= 4; i++ {
		cs = append(cs, "转色")
		cs = append(cs, "+4")
	}

	return cs
}

var cards = Cards()

// TODO 发牌
func card() string {
	//cn, _ := rand.Int(rand.Reader, big.NewInt(4))
	//c := color[cn.Int64()]
	n, _ := rand.Int(rand.Reader, big.NewInt(108))
	return cards[n.Int64()]
}