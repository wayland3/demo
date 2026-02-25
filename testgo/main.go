package main

import (
	"fmt"
	"math"
	"net/http"
)

const apiURL = "https://maque2-api.dev.haochang.tv/v2/api/user/info"

func main() {
	// 测试解码
	// dan, danScore, decimal := decodeScore(1236950583248.2046)
	// fmt.Printf("解码结果: dan=%d, danScore=%d, decimal=%d\n", dan, danScore, decimal)

	// 验证编码解码是否一致
	var dan int64 = 30
	var danScore int64 = 12345678910
	var decimal int64 = 0
	encoded := encodeScore(dan, danScore, decimal)
	fmt.Printf("重新编码: %.4f\n", encoded)
}

// 生成排序分数：dan(5bit)*2^37 + dan_score(37bit)。小数 11bit
func encodeScore(dan int64, danScore int64, decimal int64) float64 {
	return float64(dan*DanScoreMultiplier+danScore) + float64(decimal)/decimalScale
}

const (
	DanScoreMultiplier = 1 << 37 // 137438953472
	decimalScale       = 10000
)

// requestByUserIDs 循环请求，每个 id 设置 x-debug-userid 头，不处理返回值
func requestByUserIDs(ids []int64) {
	client := &http.Client{}
	for _, id := range ids {
		req, err := http.NewRequest(http.MethodGet, apiURL, nil)
		if err != nil {
			fmt.Printf("id %d new request err: %v\n", id, err)
			continue
		}
		req.Header.Set("x-debug-userid", fmt.Sprintf("%d", id))
		req.Header.Set("x-api-test", "1")
		_, err = client.Do(req) // 不处理返回值，仅调用
		if err != nil {
			fmt.Printf("id %d request err: %v\n", id, err)
			continue
		}
	}
}

func decodeScore(score float64) (dan, danScore int64, decimal int64) {
	intPart := int64(score)
	dan = intPart / DanScoreMultiplier
	danScore = intPart % DanScoreMultiplier
	// 使用 math.Modf 获取小数部分，避免浮点数精度问题
	_, frac := math.Modf(score)
	decimal = int64(math.Round(frac * decimalScale)) // 使用 Round 避免精度丢失
	return dan, danScore, decimal
}
