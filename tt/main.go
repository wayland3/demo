package main

import "log"

func main() {
	l := []int{0, 0, 0}
	l1 := l[:]
	l1[0] = 1
	log.Println("l", l)
	log.Println("l1", l1)
}
