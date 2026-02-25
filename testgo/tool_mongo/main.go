package main

import (
	"context"
	"fmt"

	_ "github.com/go-sql-driver/mysql"
	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"

	"log"

	"gorm.io/driver/mysql"
	"gorm.io/gorm"
)

type Character struct {
	ID   int64  `gorm:"column:database_id"`
	Name string `gorm:"column:name"`
}

type MongoData struct {
	ID       int64  `bson:"_id"`
	BindID   int64  `bson:"bind_id"`
	BindName string `bson:"bind_name"`
}

func main() {
	// 连接到 MySQL 数据库
	dsn := "mahjong:Mahjong#2021@tcp(10.0.1.50:3306)/game_pre_release?charset=utf8mb4&parseTime=true"
	db, err := gorm.Open(mysql.Open(dsn), &gorm.Config{})
	if err != nil {
		log.Fatal(err)
	}

	// 查询数据
	var characters []Character
	result := db.Table("character").Find(&characters)
	if result.Error != nil {
		log.Fatal(result.Error)
	}

	// 打印查询结果
	for _, character := range characters {
		log.Printf("ID: %d, Name: %s\n", character.ID, character.Name)
	}

	uri := "mongodb://admin:admin@10.0.1.54/?authSource=admin&timeout=5000"
	// uri = "mongodb://michong:michong@10.0.0.36/?authSource=admin&timeout=5000"
	opt := options.Client().ApplyURI(uri)
	opt.SetMaxPoolSize(50)

	c, err := mongo.Connect(context.Background(), opt)
	if err != nil {
		log.Fatal(err)
	}

	defer c.Disconnect(context.TODO())

	// 插入数据到 MongoDB
	collection := c.Database("game_pre_release").Collection("test_server_bind")
	for _, d := range characters {
		mongoData := &MongoData{
			ID:       d.ID,
			BindID:   d.ID,
			BindName: d.Name,
		}
		_, err := collection.InsertOne(context.TODO(), mongoData)
		if err != nil {
			log.Fatal(err)
		}
	}

	fmt.Println("Data transferred successfully.")
}
