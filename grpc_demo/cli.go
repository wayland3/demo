package main

import (
	"context"
	"ggg/services"
	"log"

	"google.golang.org/grpc"
)

func main() {
	c, err := grpc.Dial(":8081", grpc.WithInsecure())
	if err != nil {
		log.Fatal(err)
	}
	defer c.Close()

	cli := services.NewGoSpiderClient(c)
	resp, err := cli.GetAddressResponse(context.Background(), &services.SendAddress{Address: "aaa"})
	if err != nil {
		log.Fatal(err)
	}
	log.Println(resp.HttpCode)
}
