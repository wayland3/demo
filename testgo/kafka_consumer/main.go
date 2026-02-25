package main

import (
	"context"
	"errors"
	"io"
	"log"
	"time"

	"github.com/segmentio/kafka-go"
)

func main() {
	r := kafka.NewReader(kafka.ReaderConfig{
		Brokers: []string{"10.0.0.181:9092"},
		GroupID: "payGroup_test",
		Topic:   "purchase-validation-response-dev",
		MaxWait: time.Second * 3,
	})

	ctx, cancel := context.WithCancel(context.Background())
	defer cancel()
	go func() {
		for {
			msg, err := r.ReadMessage(ctx)
			log.Println(time.Now())
			log.Println(string(msg.Value), err)
			if errors.Is(err, context.Canceled) || errors.Is(err, context.DeadlineExceeded) || errors.Is(err, io.EOF) {
				break
			}
		}
	}()
	time.Sleep(time.Second)
	start := time.Now()
	log.Println(start)
	r.Close()
	time.Sleep(time.Second * 10)

	// msg, err := r.FetchMessage(ctx)
	// log.Println(msg, err)
	// r.Close()
	// time.Sleep(time.Second * 10)
	// err = r.CommitMessages(ctx, msg)
	// log.Println(err)
}
