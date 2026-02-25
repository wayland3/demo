package main

import (
	"net"
	"ttt/grpc/proto_gen/service"

	"google.golang.org/grpc"
)

type server struct {
	service.HelloServer
}

// func (s *server) T(ctx context.Context, in *ss.TRequest) (*ss.TResponse, error) {
// 	return &ss.TResponse{}, nil
// }

func main() {
	lis, err := net.Listen("tcp", ":8080")
	if err != nil {
		panic(err)
	}

	s := grpc.NewServer()
	service.RegisterHelloServer(s, &server{})

	if err := s.Serve(lis); err != nil {
		panic(err)
	}
}
