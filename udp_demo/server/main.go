package main

import (
	"log"
	"net"
)

func main() {
	conn, err := net.ListenUDP("udp", &net.UDPAddr{IP: net.IPv4(0, 0, 0, 0), Port: 3000})
	if err != nil {
		log.Fatal(err)
	}

	defer conn.Close()
	for {
		var data [1024]byte
		n, addr, err := conn.ReadFromUDP(data[:])
		if err != nil {
			log.Println("read udp errer: ", err)
			continue
		}

		log.Println(string(data[:n]), addr, n)
		_, err = conn.WriteToUDP(data[:n], addr)
		if err != nil {
			log.Println("write to udp error: ", err)
			continue
		}
	}
}
