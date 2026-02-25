package main

import (
	"flag"
	"log"
	"strings"
	"time"

	"gorm.io/driver/mysql"
	"gorm.io/gorm"
	"gorm.io/gorm/logger"
)

var (
	action = flag.String("action", "add", "行为")
	ids    = flag.String("ids", "", "用户id")
)

// im
const (
	url            = "https://adminapisgp.im.qcloud.com/v4/"
	sdk_app_id     = 20000217
	identifier     = "admin"
	sign_algorithm = "HMAC-SHA256"
	private_key    = "0da5447f302ea8c35caa52393366972c191bf40f81cb2d5d6f025ad53bb8c51a"
)

const (
	dev  = "michong:michong@tcp(10.0.0.242:3306)/video_chat?charset=utf8mb4&autocommit=true"
	test = "michong:michong@tcp(10.0.0.242:3306)/video_chat_test?charset=utf8mb4&autocommit=true"
)

func main() {
	flag.Parse()

	// im
	signature := Signature{
		SDKAppID:   sdk_app_id,
		PrivateKey: private_key,
		Algorithm:  sign_algorithm,
	}
	sign, err := signature.GenerateSign(identifier, time.Second*100)
	if err != nil {
		panic(err)
	}

	im := IM{
		SDKAppID:       sdk_app_id,
		Identifier:     identifier,
		IdentifierSign: sign,
		URL:            url,
	}

	// id
	var idList []string
	if *ids == "all" {
		dbDEV, err := gorm.Open(mysql.Open(dev), &gorm.Config{Logger: logger.Discard})
		if err != nil {
			panic("failed to connect database")
		}
		var ids []string
		if err := dbDEV.Table("users").Pluck("uid", &ids).Error; err != nil {
			panic(err)
		}
		idList = ids
		log.Println("dev user len: ", len(ids))

		ids = nil
		dbTest, err := gorm.Open(mysql.Open(test), &gorm.Config{Logger: logger.Discard})
		if err != nil {
			panic("failed to connect database")
		}
		if err := dbTest.Table("users").Pluck("uid", &ids).Error; err != nil {
			panic(err)
		}

		for _, id := range ids {
			idList = append(idList, id)
		}
		log.Println("test user len: ", len(ids))

	} else {
		idList = strings.Split(*ids, ",")
	}

	// 执行
	if *action == "add" {
		if err := im.Add(idList...); err != nil {
			panic(err)
		}
	}
	if *action == "remove" {
		if err := im.Remove(idList...); err != nil {
			panic(err)
		}
	}
}
