package fcm

import (
	"context"
	"fmt"
	"log"
	"time"

	"firebase.google.com/go/v4/messaging"
)

// PlatformConfig 平台特定配置
type PlatformConfig struct {
	// Android 配置
	Android *AndroidPlatformConfig
	// iOS 配置
	APNS *APNSPlatformConfig
	// Web 配置
	Webpush *WebpushPlatformConfig
}

// AndroidPlatformConfig Android 平台配置
type AndroidPlatformConfig struct {
	Priority             string                                // "normal" 或 "high"
	Icon                 string                                // 通知图标
	Color                string                                // 通知颜色 (#RRGGBB)
	Sound                string                                // 通知声音
	ChannelID            string                                // 通知渠道 ID
	CollapseKey          string                                // 合并键
	TTLHours             int                                   // 消息存活时间（小时）
	NotificationPriority messaging.AndroidNotificationPriority // 通知优先级
}

// APNSPlatformConfig iOS 平台配置
type APNSPlatformConfig struct {
	Badge            *int   // 角标数字
	Sound            string // 通知声音
	Category         string // 通知类别
	ContentAvailable bool   // 后台应用刷新
	MutableContent   bool   // 允许通知扩展修改
	Priority         string // "10" 或 "5"
}

// WebpushPlatformConfig Web 平台配置
type WebpushPlatformConfig struct {
	Icon               string          // 通知图标 URL
	Badge              string          // 徽章图标 URL
	Image              string          // 大图 URL
	RequireInteraction bool            // 需要用户交互
	Actions            []WebpushAction // 操作按钮
	Link               string          // 点击后跳转的链接
}

// WebpushAction Web 推送操作按钮
type WebpushAction struct {
	Action string // 操作标识符
	Title  string // 按钮文本
	Icon   string // 按钮图标 URL
}

// SendToDeviceWithPlatformConfig 向单个设备发送推送（支持平台特定配置）
func (c *Client) SendToDeviceWithPlatformConfig(token string, msg *Message, platformConfig *PlatformConfig) error {
	ctx := context.Background()

	// 基础通知
	notification := &messaging.Notification{
		Title: msg.Title,
		Body:  msg.Body,
	}

	if msg.Image != "" {
		notification.ImageURL = msg.Image
	}

	// 构建消息
	message := &messaging.Message{
		Token:        token,
		Notification: notification,
	}

	if len(msg.Data) > 0 {
		message.Data = msg.Data
	}

	// 添加 Android 配置
	if platformConfig != nil && platformConfig.Android != nil {
		androidConfig := &messaging.AndroidConfig{}

		if platformConfig.Android.Priority != "" {
			androidConfig.Priority = platformConfig.Android.Priority
		}

		if platformConfig.Android.CollapseKey != "" {
			androidConfig.CollapseKey = platformConfig.Android.CollapseKey
		}

		if platformConfig.Android.TTLHours > 0 {
			ttl := time.Duration(platformConfig.Android.TTLHours) * time.Hour
			androidConfig.TTL = &ttl
		}

		// Android 通知配置
		androidNotification := &messaging.AndroidNotification{}
		if platformConfig.Android.Icon != "" {
			androidNotification.Icon = platformConfig.Android.Icon
		}
		if platformConfig.Android.Color != "" {
			androidNotification.Color = platformConfig.Android.Color
		}
		if platformConfig.Android.Sound != "" {
			androidNotification.Sound = platformConfig.Android.Sound
		}
		if platformConfig.Android.ChannelID != "" {
			androidNotification.ChannelID = platformConfig.Android.ChannelID
		}
		if platformConfig.Android.NotificationPriority != 0 {
			androidNotification.Priority = platformConfig.Android.NotificationPriority
		}

		androidConfig.Notification = androidNotification
		message.Android = androidConfig
	}

	// 添加 iOS 配置
	if platformConfig != nil && platformConfig.APNS != nil {
		apnsConfig := &messaging.APNSConfig{}

		// Headers
		if platformConfig.APNS.Priority != "" {
			if apnsConfig.Headers == nil {
				apnsConfig.Headers = make(map[string]string)
			}
			apnsConfig.Headers["apns-priority"] = platformConfig.APNS.Priority
		}

		// Payload
		aps := &messaging.Aps{}
		if platformConfig.APNS.Badge != nil {
			aps.Badge = platformConfig.APNS.Badge
		}
		if platformConfig.APNS.Sound != "" {
			aps.Sound = platformConfig.APNS.Sound
		}
		if platformConfig.APNS.Category != "" {
			aps.Category = platformConfig.APNS.Category
		}
		if platformConfig.APNS.ContentAvailable {
			aps.ContentAvailable = true
		}
		if platformConfig.APNS.MutableContent {
			aps.MutableContent = true
		}

		apnsConfig.Payload = &messaging.APNSPayload{
			Aps: aps,
		}
		message.APNS = apnsConfig
	}

	// 添加 Web 配置
	if platformConfig != nil && platformConfig.Webpush != nil {
		webpushConfig := &messaging.WebpushConfig{}

		// 通知配置
		webpushNotification := &messaging.WebpushNotification{}
		if platformConfig.Webpush.Icon != "" {
			webpushNotification.Icon = platformConfig.Webpush.Icon
		}
		if platformConfig.Webpush.Badge != "" {
			webpushNotification.Badge = platformConfig.Webpush.Badge
		}
		if platformConfig.Webpush.Image != "" {
			webpushNotification.Image = platformConfig.Webpush.Image
		}
		webpushNotification.RequireInteraction = platformConfig.Webpush.RequireInteraction

		// 操作按钮
		if len(platformConfig.Webpush.Actions) > 0 {
			actions := make([]*messaging.WebpushNotificationAction, 0, len(platformConfig.Webpush.Actions))
			for _, action := range platformConfig.Webpush.Actions {
				actions = append(actions, &messaging.WebpushNotificationAction{
					Action: action.Action,
					Title:  action.Title,
					Icon:   action.Icon,
				})
			}
			webpushNotification.Actions = actions
		}

		webpushConfig.Notification = webpushNotification

		// FCM 选项
		if platformConfig.Webpush.Link != "" {
			webpushConfig.FCMOptions = &messaging.WebpushFCMOptions{
				Link: platformConfig.Webpush.Link,
			}
		}

		message.Webpush = webpushConfig
	}

	response, err := c.messaging.Send(ctx, message)
	if err != nil {
		return fmt.Errorf("发送推送失败: %w", err)
	}

	log.Printf("推送成功发送: %s", response)
	return nil
}

// SendHighPriorityAndroidPush 发送高优先级 Android 推送（便捷方法）
func (c *Client) SendHighPriorityAndroidPush(token string, msg *Message, icon, color, channelID string) error {
	platformConfig := &PlatformConfig{
		Android: &AndroidPlatformConfig{
			Priority:             "high",
			Icon:                 icon,
			Color:                color,
			ChannelID:            channelID,
			Sound:                "default",
			NotificationPriority: messaging.PriorityHigh,
			TTLHours:             24,
		},
	}
	return c.SendToDeviceWithPlatformConfig(token, msg, platformConfig)
}

// SendIOSPushWithBadge 发送带角标的 iOS 推送（便捷方法）
func (c *Client) SendIOSPushWithBadge(token string, msg *Message, badge int, sound string) error {
	platformConfig := &PlatformConfig{
		APNS: &APNSPlatformConfig{
			Badge:            &badge,
			Sound:            sound,
			Priority:         "10",
			ContentAvailable: false,
			MutableContent:   false,
		},
	}
	return c.SendToDeviceWithPlatformConfig(token, msg, platformConfig)
}

// SendWebPushWithActions 发送带操作按钮的 Web 推送（便捷方法）
func (c *Client) SendWebPushWithActions(token string, msg *Message, iconURL string, actions []WebpushAction, link string) error {
	platformConfig := &PlatformConfig{
		Webpush: &WebpushPlatformConfig{
			Icon:               iconURL,
			Actions:            actions,
			Link:               link,
			RequireInteraction: false,
		},
	}
	return c.SendToDeviceWithPlatformConfig(token, msg, platformConfig)
}

