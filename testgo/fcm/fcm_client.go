package fcm

import (
	"context"
	"fmt"
	"log"

	firebase "firebase.google.com/go/v4"
	"firebase.google.com/go/v4/messaging"
	"google.golang.org/api/option"
)

// Message 推送消息结构
type Message struct {
	Title string            // 通知标题
	Body  string            // 通知内容
	Image string            // 通知图片URL（可选）
	Data  map[string]string // 自定义数据（可选）
}

// Client FCM 客户端
type Client struct {
	messaging *messaging.Client
}

// NewClient 创建 FCM 客户端
// credentialsPath: 服务账号密钥文件路径，如果为空则使用环境变量 GOOGLE_APPLICATION_CREDENTIALS
func NewClient(credentialsPath string) (*Client, error) {
	ctx := context.Background()

	var opts []option.ClientOption
	if credentialsPath != "" {
		opts = append(opts, option.WithCredentialsFile(credentialsPath))
	}
	app, err := firebase.NewApp(ctx, nil, opts...)
	if err != nil {
		return nil, fmt.Errorf("初始化 Firebase 应用失败: %w", err)
	}

	messagingClient, err := app.Messaging(ctx)
	if err != nil {
		return nil, fmt.Errorf("创建 Messaging 客户端失败: %w", err)
	}

	return &Client{
		messaging: messagingClient,
	}, nil
}

// SendToDevice 向单个设备发送推送
func (c *Client) SendToDevice(token string, msg *Message) error {
	ctx := context.Background()

	notification := &messaging.Notification{
		Title: msg.Title,
		Body:  msg.Body,
	}

	if msg.Image != "" {
		notification.ImageURL = msg.Image
	}

	message := &messaging.Message{
		Token:        token,
		Notification: notification,
	}

	if len(msg.Data) > 0 {
		message.Data = msg.Data
	}

	response, err := c.messaging.Send(ctx, message)
	if err != nil {
		return fmt.Errorf("发送推送失败: %w", err)
	}

	log.Printf("推送成功发送: %s", response)
	return nil
}

// SendToMultipleDevices 向多个设备发送推送（最多1000个设备）
func (c *Client) SendToMultipleDevices(tokens []string, msg *Message) (*messaging.BatchResponse, error) {
	if len(tokens) == 0 {
		return nil, fmt.Errorf("设备 token 列表为空")
	}

	if len(tokens) > 1000 {
		return nil, fmt.Errorf("设备 token 数量超过限制（最大1000个）")
	}

	ctx := context.Background()

	notification := &messaging.Notification{
		Title: msg.Title,
		Body:  msg.Body,
	}

	if msg.Image != "" {
		notification.ImageURL = msg.Image
	}

	message := &messaging.MulticastMessage{
		Tokens:       tokens,
		Notification: notification,
	}

	if len(msg.Data) > 0 {
		message.Data = msg.Data
	}

	response, err := c.messaging.SendEachForMulticast(ctx, message)
	if err != nil {
		return nil, fmt.Errorf("批量发送推送失败: %w", err)
	}

	log.Printf("批量推送完成: 成功 %d, 失败 %d", response.SuccessCount, response.FailureCount)

	// 检查并记录失败的 token
	if response.FailureCount > 0 {
		for i, resp := range response.Responses {
			if !resp.Success {
				log.Printf("推送失败 - Token: %s, 错误: %v", tokens[i], resp.Error)
			}
		}
	}

	return response, nil
}

// SendToTopic 向订阅某个主题的所有设备发送推送
func (c *Client) SendToTopic(topic string, msg *Message) error {
	ctx := context.Background()

	notification := &messaging.Notification{
		Title: msg.Title,
		Body:  msg.Body,
	}

	if msg.Image != "" {
		notification.ImageURL = msg.Image
	}

	message := &messaging.Message{
		Topic:        topic,
		Notification: notification,
	}

	if len(msg.Data) > 0 {
		message.Data = msg.Data
	}

	response, err := c.messaging.Send(ctx, message)
	if err != nil {
		return fmt.Errorf("发送主题推送失败: %w", err)
	}

	log.Printf("主题推送成功: %s", response)
	return nil
}

// SubscribeToTopic 订阅主题
func (c *Client) SubscribeToTopic(tokens []string, topic string) error {
	ctx := context.Background()

	if len(tokens) == 0 {
		return fmt.Errorf("设备 token 列表为空")
	}

	response, err := c.messaging.SubscribeToTopic(ctx, tokens, topic)
	if err != nil {
		return fmt.Errorf("订阅主题失败: %w", err)
	}

	log.Printf("主题订阅结果: 成功 %d, 失败 %d", response.SuccessCount, response.FailureCount)

	if response.FailureCount > 0 {
		for i, err := range response.Errors {
			log.Printf("订阅失败 - Token: %s, 错误: %v", tokens[i], err)
		}
	}

	return nil
}

// UnsubscribeFromTopic 取消订阅主题
func (c *Client) UnsubscribeFromTopic(tokens []string, topic string) error {
	ctx := context.Background()

	if len(tokens) == 0 {
		return fmt.Errorf("设备 token 列表为空")
	}

	response, err := c.messaging.UnsubscribeFromTopic(ctx, tokens, topic)
	if err != nil {
		return fmt.Errorf("取消订阅主题失败: %w", err)
	}

	log.Printf("取消订阅结果: 成功 %d, 失败 %d", response.SuccessCount, response.FailureCount)

	if response.FailureCount > 0 {
		for i, err := range response.Errors {
			log.Printf("取消订阅失败 - Token: %s, 错误: %v", tokens[i], err)
		}
	}

	return nil
}

// SendConditionalMessage 发送条件推送（基于主题条件表达式）
// 例如: "'stock-GOOG' in topics || 'stock-AAPL' in topics"
func (c *Client) SendConditionalMessage(condition string, msg *Message) error {
	ctx := context.Background()

	notification := &messaging.Notification{
		Title: msg.Title,
		Body:  msg.Body,
	}

	if msg.Image != "" {
		notification.ImageURL = msg.Image
	}

	message := &messaging.Message{
		Condition:    condition,
		Notification: notification,
	}

	if len(msg.Data) > 0 {
		message.Data = msg.Data
	}

	response, err := c.messaging.Send(ctx, message)
	if err != nil {
		return fmt.Errorf("发送条件推送失败: %w", err)
	}

	log.Printf("条件推送成功: %s", response)
	return nil
}
