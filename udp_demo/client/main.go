package main

import (
	"log"
	"net"
)

func main() {
	conn, err := net.DialUDP("udp", nil, &net.UDPAddr{IP: net.IPv4(0, 0, 0, 0), Port: 3000})
	if err != nil {
		log.Fatal(err)
	}

	defer conn.Close()
	data := []byte("abc")
	_, err = conn.Write(data)
	if err != nil {
		log.Println("write error: ", err)
		return
	}

	data = make([]byte, 1024)
	n, rAddr, err := conn.ReadFromUDP(data)
	if err != nil {
		log.Println("read udp err: ", err)
		return
	}

	log.Printf("recv: %s, addr: %v, count: %v", string(data[:n]), rAddr, n)

}
