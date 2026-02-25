package main

import (
	"context"
	"time"
	"ttt/grpc/proto_gen/cs"
	"ttt/grpc/proto_gen/service"

	"google.golang.org/grpc"
)

func main() {
	conn, err := grpc.Dial("localhost:8080", grpc.WithInsecure())
	if err != nil {
		panic(err)
	}

	defer conn.Close()

	c := service.NewHelloClient(conn)
	ctx, cancel := context.WithTimeout(context.Background(), time.Second)
	defer cancel()

	cs := cs.CS{
		Id: "hello",
	}

	r, err := c.Get(ctx, &cs)
	if err != nil {
		panic(err)
	}

	println(r.Cs)
}
