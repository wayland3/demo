package main

import (
	_ "net/http/pprof"
)

var ch chan int

func main() {
	// cpu
	// f, err := os.Create("cpu.pprof")
	// if err != nil {
	// 	log.Fatal(err)
	// }
	// defer f.Close()

	// pprof.StartCPUProfile(f)
	// log.Println(test(50))
	// pprof.StopCPUProfile()

	// mem
	// f, err := os.Create("mem.pprof")
	// if err != nil {
	// 	log.Fatal(err)
	// }
	// defer f.Close()
	// log.Println(test(50))
	// _ = make([]int, 100000000)
	// pprof.WriteHeapProfile(f)

	// server

}

func test(n int) int {
	if n == 0 {
		return 0
	}
	if n == 1 {
		return 1
	}
	return test(n-1) + test(n-2)
}

func fib(n int) int {
	if n == 1 {
		return 1
	}

	if n < 1 {
		return 0
	}

	fib := make([]int, n+1)
	fib[0] = 0
	fib[1] = 1

	for i := 2; i <= n; i++ {
		fib[i] = fib[i-2] + fib[i-1]
	}
	return fib[n]
}
