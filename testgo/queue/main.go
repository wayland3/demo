package main

import (
	"fmt"
	"log"
	"math/rand"
	"sync"
	"time"

	"github.com/reactivex/rxgo/v2"
)

// Queue 实现按时间或者数量获取元素的缓冲队列
// 当队列中的元素数量达到指定数量或者指定时间后
// 会将队列中的元素作为切片一次性返回
type Queue struct {
	pool     chan any
	len      int           // 0 表示不限制
	duration time.Duration // 0 表示不限制
}

// New 创建
func New(poolSize, len int, duration time.Duration) *Queue {
	return &Queue{pool: make(chan any, poolSize), len: len, duration: duration}
}

// Close 关闭队列
func (q *Queue) Close() {
	close(q.pool)
}

// Push 将元素放入队列
func (q *Queue) Push(item any) {
	q.pool <- item
}

// Buffer 返回切片类型的channel
func (q *Queue) Buffer() <-chan any {
	mu := &sync.Mutex{}
	ch := make(chan any, 1)
	buffer := make([]any, 0, q.len)
	send := make(chan struct{})
	stop := make(chan struct{})

	checkSend := func() {
		mu.Lock()
		if len(buffer) > 0 {
			ch <- buffer
			buffer = make([]any, 0, q.len)
		}
		mu.Unlock()
	}

	go func() {
		defer func() {
			close(send)
			close(ch)
		}()

		for {
			select {
			case <-send:
				checkSend()
			case <-time.After(q.duration):
				checkSend()
			case <-stop:
				checkSend()
				return
			}
		}
	}()

	go func() {
		for {
			item, ok := <-q.pool
			if !ok {
				close(stop)
				return
			}
			mu.Lock()
			buffer = append(buffer, item)
			if len(buffer) == q.len {
				send <- struct{}{}
			}
			mu.Unlock()
		}
	}()

	return ch
}

func pushQ(q *Queue) {
	list := []any{1, 2, 3, 4, 5, 6, 7, 8, 9, 10}

	for _, item := range list {
		n := rand.Intn(5)
		time.Sleep(time.Second * time.Duration(n)) // 模拟耗时操作
		q.Push(item)
	}
	q.Close()
}

func main() {
	q := New(1000, 5, 2*time.Second)
	go pushQ(q)

	log.Println("start")
	for v := range q.Buffer() {
		log.Println(time.Now(), v)
	}
}

// 基于rxgo
// ----------------------------
func push(ch chan<- rxgo.Item) {
	list := []any{1, 2, 3, 4, 5, 6, 7, 8, 9, 10}

	for _, item := range list {
		n := rand.Intn(5)
		time.Sleep(time.Second * time.Duration(n)) // 模拟耗时操作
		ch <- rxgo.Of(item)
	}
	close(ch)
}

func main1() {
	ch := make(chan rxgo.Item, 10)

	observable := rxgo.FromChannel(ch)
	go push(ch)

	// 2秒钟缓冲一次，或者缓冲3个数据
	observable = observable.BufferWithTimeOrCount(rxgo.WithDuration(2*time.Second), 3)

	for item := range observable.Observe() {
		fmt.Println(item.V)
	}
}
