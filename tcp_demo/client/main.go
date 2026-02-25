package main

import (
	"bytes"
	"encoding/binary"
	"log"
	"net"
	"time"
)

func Encode(message string) ([]byte, error) {
	length := int32(len(message))
	pkg := new(bytes.Buffer)
	// 写入头
	err := binary.Write(pkg, binary.LittleEndian, length)
	if err != nil {
		return nil, err
	}
	// 写入体
	err = binary.Write(pkg, binary.LittleEndian, []byte(message))
	if err != nil {
		return nil, err
	}

	return pkg.Bytes(), nil
}

func main() {
	send()
	time.Sleep(time.Second)
	send()
}
func send() {
	conn, err := net.Dial("tcp", "127.0.0.1:3000")
	if err != nil {
		log.Fatal(err)
	}

	b := []byte("abc")
	n, err := conn.Write(b)
	log.Println("send:", n, err)
	time.Sleep(time.Second)

	// msg := "abc"
	// for i := 0; i < 20; i++ {
	// 	b, _ := Encode(msg + strconv.FormatInt(int64(i), 10))
	// 	n, err := conn.Write(b)
	// 	if err != nil {
	// 		log.Fatal(err)
	// 	}

	// 	log.Println("send:", n, i)
	// }

	// time.Sleep(time.Second * 10)
	// if err := conn.Close(); err != nil {
	// 	log.Fatal(err)
	// }

	// log.Println("close")
}
