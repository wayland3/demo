package main

import (
	"bufio"
	"bytes"
	"context"
	"encoding/binary"
	"log"
	"time"

	"github.com/cloudwego/netpoll"
)

const lenNum = 4

func Decode(reader *bufio.Reader) (string, error) {
	// 读取长度
	lengthByte, err := reader.Peek(lenNum)
	if err != nil {
		return "", err
	}

	lengthReader := bytes.NewReader(lengthByte)
	var length int32
	err = binary.Read(lengthReader, binary.LittleEndian, &length)
	if err != nil {
		return "", err
	}

	// 缓冲区长度
	if int32(reader.Buffered()) < length+lenNum {
		return "", nil
	}

	pkg := make([]byte, int(length+lenNum))
	_, err = reader.Read(pkg)
	if err != nil {
		return "", err
	}
	return string(pkg[lenNum:]), nil
}

func main() {
	// netpoll.
	listen, err := netpoll.CreateListener("tcp", ":3000")
	if err != nil {
		log.Fatal(err)
	}

	defer listen.Close()

	eventLoop, err := netpoll.NewEventLoop(
		handle,
		netpoll.WithReadTimeout(time.Second),
	)

	eventLoop.Serve(listen)

	// for {
	// 	conn, err := listen.Accept()
	// 	if err != nil {
	// 		log.Println("accept error")
	// 		continue
	// 	}

	// 	go process(conn)
	// }
}

func handle(ctx context.Context, connection netpoll.Connection) error {
	log.Println(connection.RemoteAddr())
	return nil
}

func process(conn netpoll.Conn) {
	conn.Close()
	log.Println(conn.RemoteAddr())
	time.Sleep(time.Minute)
	n, err := conn.Write([]byte("hello"))
	log.Println(n, err)
}
