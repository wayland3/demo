package main

import (
	"go_sort/sort_func"
	"log"
)

var toSort = []int{1, 16, 6, 3, 9}

func main() {
	sort_func.Quick(toSort, 0, len(toSort)-1)
	log.Println(toSort)
}
