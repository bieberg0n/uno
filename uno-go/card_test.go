package main

import "testing"

func TestCards(t *testing.T) {
	cs := Cards()
	logs(len(cs))
	logs(cs)
}
