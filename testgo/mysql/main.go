package main

import (
	"log"
	"sync"
	"sync/atomic"

	jsoniter "github.com/json-iterator/go"
	"gorm.io/driver/mysql"
	"gorm.io/gorm"
	"gorm.io/gorm/logger"
)

type Character struct {
	DatabaseID int64  `gorm:"column:database_id;primaryKey"`
	Inv        string `gorm:"column:inventory"`
}

func (Character) TableName() string {
	return "character"
}

var (
	ch chan *Character = make(chan *Character, 10000)
	wg                 = &sync.WaitGroup{}
	db *gorm.DB
)

func init() {
	dsn := "root:Mahjong2021@tcp(172.31.11.159)/game?charset=utf8mb4&parseTime=True&loc=Local"
	dsn = "michong:michong@tcp(10.0.0.241)/mahjong_game_test?charset=utf8mb4&parseTime=True&loc=Local"
	dsn = "mahjong:Mahjong#2021@tcp(mahjong-golang-test-mysql-slb.mysql.svc.cluster.local:3306)/game_test?charset=utf8mb4&parseTime=True&loc=Local"

	var err error
	db, err = gorm.Open(mysql.Open(dsn), &gorm.Config{
		Logger: logger.Default.LogMode(logger.Silent),
	})
	if err != nil {
		log.Fatal("Failed to connect to database: ", err)
	}
}

var (
	playerCount = atomic.Int64{}
	totalCount  = atomic.Int64{}
)

type Item struct {
	ID    string `json:"1"`
	Count int64  `json:"2"`
}

func check() {
	for c := range ch {
		bs := jsoniter.Get([]byte(c.Inv), "1")
		if bs == nil {
			continue
		}

		var items []Item
		bs.ToVal(&items)

		for _, item := range items {
			if item.ID == "OTKVoucher" {
				playerCount.Add(1)
				totalCount.Add(item.Count)
			}
		}
	}
	wg.Done()
}

func main() {
	log.Println("start")
	for i := 0; i < 2; i++ {
		check()
		wg.Add(1)
	}

	const batchSize = 1000
	var users []*Character
	err := db.FindInBatches(&users, batchSize, func(tx *gorm.DB, batch int) error {
		log.Println("batch:", batch)
		for _, user := range users {
			ch <- user
		}
		return nil
	}).Error
	if err != nil {
		log.Fatal("Failed to connect to database: ", err)
	}

	close(ch)
	wg.Wait()

	log.Println("playerCount:", playerCount.Load(), "totalCount:", totalCount.Load())
	log.Println("end")
}
