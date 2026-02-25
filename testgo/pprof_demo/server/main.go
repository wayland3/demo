package main

import "net/http"
import _ "net/http/pprof"

var a []int

func main() {
	a = make([]int, 9999999)

	http.HandleFunc("/test", func(w http.ResponseWriter, r *http.Request) {
		var s []int
		for i := 0; i < 10000; i++ {
			s = append(s, i)
		}

		w.Write([]byte("abc"))
	})
	http.ListenAndServe(":8080", nil)
}
