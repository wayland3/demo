# 平台特定配置使用指南

## 一、快速开始

### 场景 1: 发送高优先级 Android 推送

```go
package main

import (
    "log"
    "os"
    "ttt/fcm"
)

func main() {
    client, err := fcm.NewClient(os.Getenv("GOOGLE_APPLICATION_CREDENTIALS"))
    if err != nil {
        log.Fatalf("创建客户端失败: %v", err)
    }

    token := "用户的FCM设备Token"
    
    // 发送高优先级 Android 推送
    err = client.SendHighPriorityAndroidPush(
        token,
        &fcm.Message{
            Title: "重要通知",
            Body:  "这是一条高优先级推送",
            Data: map[string]string{
                "type": "urgent",
            },
        },
        "important_icon",      // 通知图标
        "#FF0000",             // 红色通知栏
        "critical_channel",    // 通知渠道
    )
    
    if err != nil {
        log.Printf("发送失败: %v", err)
    }
}
```

### 场景 2: 发送带角标的 iOS 推送

```go
// 发送带角标的 iOS 推送
badgeCount := 5
err = client.SendIOSPushWithBadge(
    token,
    &fcm.Message{
        Title: "新消息",
        Body:  "您有 5 条未读消息",
    },
    badgeCount,              // 角标数字
    "notification.wav",      // 自定义声音
)

if err != nil {
    log.Printf("发送失败: %v", err)
}
```

### 场景 3: 发送带操作按钮的 Web 推送

```go
// 发送带操作按钮的 Web 推送
actions := []fcm.WebpushAction{
    {Action: "view", Title: "查看详情", Icon: "https://example.com/view.png"},
    {Action: "dismiss", Title: "忽略", Icon: "https://example.com/dismiss.png"},
}

err = client.SendWebPushWithActions(
    token,
    &fcm.Message{
        Title: "新订单",
        Body:  "您有一个新订单待处理",
    },
    "https://example.com/icon.png",  // 通知图标
    actions,                          // 操作按钮
    "https://example.com/order/123",  // 点击后跳转的链接
)

if err != nil {
    log.Printf("发送失败: %v", err)
}
```

## 二、完整平台配置示例

### 示例：为所有平台配置不同的行为

```go
package main

import (
    "log"
    "os"
    "ttt/fcm"
    "firebase.google.com/go/v4/messaging"
)

func main() {
    client, err := fcm.NewClient(os.Getenv("GOOGLE_APPLICATION_CREDENTIALS"))
    if err != nil {
        log.Fatalf("创建客户端失败: %v", err)
    }

    token := "用户的FCM设备Token"
    
    // 构建平台特定配置
    platformConfig := &fcm.PlatformConfig{
        // Android 配置
        Android: &fcm.AndroidPlatformConfig{
            Priority:              "high",
            Icon:                  "app_icon",
            Color:                 "#4CAF50",
            Sound:                 "default",
            ChannelID:             "default_channel",
            CollapseKey:           "message_update",
            TTLHours:              24,
            NotificationPriority: messaging.PriorityHigh,
        },
        // iOS 配置
        APNS: &fcm.APNSPlatformConfig{
            Badge:            func() *int { b := 1; return &b }(),
            Sound:            "default",
            Category:         "MESSAGE_CATEGORY",
            Priority:         "10",
            ContentAvailable: false,
            MutableContent:   false,
        },
        // Web 配置
        Webpush: &fcm.WebpushPlatformConfig{
            Icon: "https://example.com/icon.png",
            Badge: "https://example.com/badge.png",
            Image: "https://example.com/image.jpg",
            RequireInteraction: false,
            Actions: []fcm.WebpushAction{
                {Action: "view", Title: "查看", Icon: "https://example.com/view.png"},
            },
            Link: "https://example.com/notification",
        },
    }
    
    // 发送消息
    err = client.SendToDeviceWithPlatformConfig(
        token,
        &fcm.Message{
            Title: "跨平台推送",
            Body:  "这条消息在不同平台有不同表现",
            Data: map[string]string{
                "type": "notification",
            },
        },
        platformConfig,
    )
    
    if err != nil {
        log.Printf("发送失败: %v", err)
    }
}
```

## 三、根据平台动态配置

```go
func sendMessageByPlatform(client *fcm.Client, token string, platform string, msg *fcm.Message) error {
    var platformConfig *fcm.PlatformConfig
    
    switch platform {
    case "android":
        platformConfig = &fcm.PlatformConfig{
            Android: &fcm.AndroidPlatformConfig{
                Priority: "high",
                Icon:     "android_icon",
                Color:    "#2196F3",
            },
        }
    case "ios":
        badge := 1
        platformConfig = &fcm.PlatformConfig{
            APNS: &fcm.APNSPlatformConfig{
                Badge:   &badge,
                Sound:   "default",
                Priority: "10",
            },
        }
    case "web":
        platformConfig = &fcm.PlatformConfig{
            Webpush: &fcm.WebpushPlatformConfig{
                Icon: "https://example.com/web-icon.png",
            },
        }
    default:
        // 不设置平台配置，使用默认行为
        platformConfig = nil
    }
    
    return client.SendToDeviceWithPlatformConfig(token, msg, platformConfig)
}
```

## 四、对比：使用平台配置 vs 不使用

### 不使用平台配置（当前代码）

```go
// 简单，但功能有限
client.SendToDevice(token, &fcm.Message{
    Title: "通知",
    Body:  "内容",
})
```

**结果**：
- ✅ 所有平台都能收到
- ❌ 无法定制 Android 图标和颜色
- ❌ 无法设置 iOS 角标
- ❌ 无法添加 Web 操作按钮
- ❌ 所有平台使用相同的优先级

### 使用平台配置（新功能）

```go
// 复杂，但功能丰富
platformConfig := &fcm.PlatformConfig{
    Android: &fcm.AndroidPlatformConfig{
        Priority: "high",
        Icon:     "custom_icon",
        Color:    "#FF0000",
    },
    APNS: &fcm.APNSPlatformConfig{
        Badge: &badgeCount,
    },
    Webpush: &fcm.WebpushPlatformConfig{
        Icon: "https://example.com/icon.png",
        Actions: []fcm.WebpushAction{
            {Action: "view", Title: "查看"},
        },
    },
}
client.SendToDeviceWithPlatformConfig(token, msg, platformConfig)
```

**结果**：
- ✅ 所有平台都能收到
- ✅ Android 使用自定义图标和颜色
- ✅ iOS 显示角标数字
- ✅ Web 有操作按钮
- ✅ 不同平台可以使用不同优先级

## 五、常见使用场景

### 场景 1: 聊天应用消息推送

```go
// Android: 显示头像图标和通知颜色
// iOS: 显示未读消息数角标
// Web: 添加"回复"和"忽略"按钮
platformConfig := &fcm.PlatformConfig{
    Android: &fcm.AndroidPlatformConfig{
        Icon:  "chat_icon",
        Color: "#2196F3",
    },
    APNS: &fcm.APNSPlatformConfig{
        Badge: &unreadCount,
    },
    Webpush: &fcm.WebpushPlatformConfig{
        Actions: []fcm.WebpushAction{
            {Action: "reply", Title: "回复"},
            {Action: "dismiss", Title: "忽略"},
        },
    },
}
```

### 场景 2: 订单状态更新

```go
// Android: 高优先级，红色通知
// iOS: 静默更新（不打扰用户）
// Web: 显示订单图片
platformConfig := &fcm.PlatformConfig{
    Android: &fcm.AndroidPlatformConfig{
        Priority: "high",
        Color:    "#FF0000",
    },
    APNS: &fcm.APNSPlatformConfig{
        Priority: "5",  // 低优先级，静默
    },
    Webpush: &fcm.WebpushPlatformConfig{
        Image: "https://example.com/order-image.jpg",
    },
}
```

### 场景 3: 新闻推送

```go
// 所有平台: 显示新闻图片，添加"阅读"按钮
platformConfig := &fcm.PlatformConfig{
    Android: &fcm.AndroidPlatformConfig{
        Icon: "news_icon",
    },
    Webpush: &fcm.WebpushPlatformConfig{
        Image: "https://example.com/news-image.jpg",
        Actions: []fcm.WebpushAction{
            {Action: "read", Title: "阅读全文"},
        },
        Link: "https://example.com/news/123",
    },
}
```

## 六、最佳实践

### 1. 渐进式迁移

不要一次性重写所有代码，可以：

```go
// 保持现有方法不变
func (c *Client) SendToDevice(token string, msg *Message) error {
    // 原有实现
}

// 新增支持平台配置的方法
func (c *Client) SendToDeviceWithPlatformConfig(...) error {
    // 新实现
}
```

### 2. 使用便捷方法

为常见场景创建便捷方法：

```go
// 高优先级推送
client.SendHighPriorityAndroidPush(...)

// 带角标的推送
client.SendIOSPushWithBadge(...)

// 带操作按钮的推送
client.SendWebPushWithActions(...)
```

### 3. 配置复用

将常用配置提取为常量或函数：

```go
func GetDefaultAndroidConfig() *AndroidPlatformConfig {
    return &AndroidPlatformConfig{
        Priority: "normal",
        Icon:     "default_icon",
        Color:    "#4CAF50",
        ChannelID: "default_channel",
    }
}
```

## 七、总结

| 特性           | 不使用平台配置 | 使用平台配置 |
|----------------|----------------|--------------|
| **代码复杂度** | 简单           | 较复杂       |
| **功能**       | 基础           | 丰富         |
| **跨平台统一** | ✅ 完全统一     | ⚠️ 可定制     |
| **用户体验**   | 基础           | 优秀         |
| **适用场景**   | 简单推送需求   | 专业应用     |

**建议**：
- 简单应用：使用当前代码（通用配置）
- 专业应用：使用平台特定配置
- 可以两者结合：基础推送用通用配置，重要推送用平台配置


