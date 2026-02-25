package main

import (
	"log"
	"time"

	jsoniter "github.com/json-iterator/go"
	"gorm.io/driver/clickhouse"
	"gorm.io/gorm"
)

type Character struct {
	DatabaseID int64  `gorm:"column:database_id;primaryKey"`
	Misc       string `gorm:"column:misc"`
}

func (Character) TableName() string {
	return "character"
}

type Event struct {
	EventTime time.Time `gorm:"column:event_time"`
	EventName string    `gorm:"column:event_name"`
	RoleID    int64     `gorm:"column:role_id"`
	EventArg3 int32     `gorm:"column:event_arg3"`
	EventArg4 int32     `gorm:"column:event_arg4"`
}

func (Event) TableName() string {
	return "event_log"
}

var (
	chDB    *gorm.DB
	mysqlDB *gorm.DB
)

var (
	betStartTS   = 1723215600
	betStartTime = time.Date(2024, 8, 9, 22, 0, 0, 0, time.Local)
	betEndTS     = 1723894200
	betEndTime   = time.Date(2024, 8, 17, 20, 30, 0, 0, time.Local)
)

func init() {
	// dsn := "root:Mahjong2021@tcp(172.31.11.159)/game?charset=utf8mb4&parseTime=True&loc=Local"
	// dsn = "michong:michong@tcp(10.0.0.241)/mahjong_game_test?charset=utf8mb4&parseTime=True&loc=Local"
	// dsn = "mahjong:Mahjong#2021@tcp(mahjong-golang-test-mysql-slb.mysql.svc.cluster.local:3306)/game_test?charset=utf8mb4&parseTime=True&loc=Local"

	// chDSN := "tcp://172.31.11.159:9001?username=mahjong&password=Mahjong2021&read_timeout=10s"
	chDSN := "tcp://172.31.11.159:9000?username=root&password=Mahjong2021&read_timeout=10s"

	var err error
	chDB, err = gorm.Open(clickhouse.Open(chDSN), &gorm.Config{})

	if err != nil {
		panic(err)
	}
}

func main() {
	log.Println("start")

	type B struct {
		I int
	}

	type A struct {
		B *B
	}

	a := A{
		B: &B{I: 1},
	}

	log.Printf("%v", a)

	return

	total := make([]*Event, 0)
	// for {
	// 	log.Println("begin time: ", betStartTime)
	var es []*Event
	err := chDB.Table("log_jp_sync.event_log").Where("event_time >= ? and event_time < ? and event_name = 'activityBet'", betStartTime, betEndTime).Find(&es).Error
	// err := chDB.Table("log.event_log").Where("event_time >= ? and event_time < ? and event_name = ?", betStartTime, betEndTime, "activityBet").Find(&es).Error
	if err != nil {
		panic(err)
	}
	total = append(total, es...)
	// if betStartTime.After(betEndTime) {
	// 	break
	// }
	// betStartTime = betStartTime.Add(time.Hour * 24)
	// }

	m := make(map[int64]map[int32]int32)
	for _, e := range total {
		if _, ok := m[e.RoleID]; !ok {
			m[e.RoleID] = make(map[int32]int32)
		}
		m[e.RoleID][e.EventArg3] += e.EventArg4
	}

	str, err := jsoniter.MarshalToString(m)
	if err != nil {
		panic(err)
	}

	log.Println(str)
	log.Println("end")
}
