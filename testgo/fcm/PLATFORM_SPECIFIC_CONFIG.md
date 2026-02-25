# FCM 平台特定配置说明

## 一、概述

`messaging.Message` 结构体中包含三个平台特定的配置字段：
- **`Android`**: Android 平台特定的配置选项
- **`APNS`**: Apple Push Notification Service (iOS) 平台特定的配置选项
- **`Webpush`**: Web 推送协议特定的配置选项

这些字段允许你为不同的平台定制推送消息的行为和外观。

## 二、为什么当前代码没有使用这些字段？

### 当前实现方式

当前代码使用的是**通用配置**：

```go
message := &messaging.Message{
    Token:        token,
    Notification: notification,  // 通用通知，所有平台使用相同的标题和内容
    Data:         data,          // 通用数据字段
}
```

### 为什么这样设计？

1. **简单性优先**
   - 对于大多数基本推送场景，使用 `Notification` 字段就足够了
   - FCM 会自动将通用通知转换为各平台支持的格式

2. **跨平台统一**
   - 不需要为每个平台写不同的代码
   - 一个消息可以同时发送给 Android、iOS 和 Web 客户端

3. **默认行为通常足够**
   - FCM 会根据设备类型自动选择合适的行为
   - 大多数应用不需要平台特定的定制

### 当前代码的局限性

当前实现方式虽然简单，但有以下限制： 

| 限制项                    | 说明                              |
|---------------------------|-----------------------------------|
| 无法定制 Android 通知样式 | 无法设置通知图标、颜色、优先级等  |
| 无法定制 iOS 通知行为     | 无法设置角标、声音、类别等        |
| 无法定制 Web 推送         | 无法设置 Web 通知图标、操作按钮等 |
| 无法精细控制推送优先级    | 所有平台使用相同的优先级策略      |

## 三、什么时候需要使用平台特定配置？

### 需要使用的场景

#### 1. **Android 特定需求**

```go
// 需要设置通知图标、颜色、优先级时
androidConfig := &messaging.AndroidConfig{
    Priority: "high",  // 高优先级推送
    Notification: &messaging.AndroidNotification{
        Icon:  "notification_icon",
        Color: "#FF0000",  // 红色通知栏颜色
        Sound: "default",
        ChannelID: "important_channel",
    },
    TTL: &time.Duration{4 * time.Hour},  // 消息存活时间
}
```

#### 2. **iOS 特定需求**

```go
// 需要设置角标、声音、类别时
apnsConfig := &messaging.APNSConfig{
    Headers: map[string]string{
        "apns-priority": "10",  // 高优先级
        "apns-expiration": "0",  // 立即发送
    },
    Payload: &messaging.APNSPayload{
        Aps: &messaging.Aps{
            Badge: &badgeCount,  // 应用角标数字
            Sound: "notification.wav",
            Category: "MESSAGE_CATEGORY",
            ContentAvailable: true,  // 后台更新
            MutableContent: true,    // 允许通知扩展修改
        },
    },
}
```

#### 3. **Web 特定需求**

```go
// 需要设置 Web 通知图标、操作按钮时
webpushConfig := &messaging.WebpushConfig{
    Notification: &messaging.WebpushNotification{
        Icon: "https://example.com/icon.png",
        Badge: "https://example.com/badge.png",
        Actions: []*messaging.WebpushNotificationAction{
            {Action: "view", Title: "查看"},
            {Action: "dismiss", Title: "忽略"},
        },
        RequireInteraction: true,  // 需要用户交互才能关闭
    },
    FCMOptions: &messaging.WebpushFCMOptions{
        Link: "https://example.com/notification-page",
    },
}
```

#### 4. **多平台同时发送，但需要不同行为**

```go
// 同一个消息，不同平台有不同行为
message := &messaging.Message{
    Token: token,  // 设备 token（FCM 会自动识别平台）
    Notification: &messaging.Notification{
        Title: "新消息",
        Body:  "您有一条新消息",
    },
    Android: &messaging.AndroidConfig{
        Priority: "high",
        Notification: &messaging.AndroidNotification{
            Icon: "msg_icon",
            Color: "#2196F3",
        },
    },
    APNS: &messaging.APNSConfig{
        Payload: &messaging.APNSPayload{
            Aps: &messaging.Aps{
                Badge: &badgeCount,
                Sound: "message.wav",
            },
        },
    },
    Webpush: &messaging.WebpushConfig{
        Notification: &messaging.WebpushNotification{
            Icon: "https://example.com/web-icon.png",
        },
    },
}
```

## 四、各平台配置详细说明

### 1. Android 配置 (`AndroidConfig`)

#### 主要字段

| 字段                    | 类型                 | 说明                                       | 示例                   |
|-------------------------|----------------------|--------------------------------------------|------------------------|
| `Priority`              | string               | 消息优先级：`"normal"` 或 `"high"`         | `"high"`               |
| `TTL`                   | *time.Duration       | 消息存活时间，超过此时间未送达则丢弃       | `4 * time.Hour`        |
| `CollapseKey`           | string               | 合并键，相同键的消息会合并（只保留最新的） | `"update_user_status"` |
| `RestrictedPackageName` | string               | 限制接收应用的包名                         | `"com.example.app"`    |
| `DirectBootOK`          | bool                 | 是否允许在直接启动模式（设备重启后）发送   | `true`                 |
| `Notification`          | *AndroidNotification | Android 通知特定配置                       | 见下表                 |

#### AndroidNotification 主要字段

| 字段          | 类型                          | 说明                                   | 示例                                |
|---------------|-------------------------------|----------------------------------------|-------------------------------------|
| `Icon`        | string                        | 通知图标资源名                         | `"notification_icon"`               |
| `Color`       | string                        | 通知栏颜色（#RRGGBB 格式）             | `"#FF0000"`                         |
| `Sound`       | string                        | 通知声音                               | `"default"` 或 `"notification.wav"` |
| `Tag`         | string                        | 通知标签，相同标签的通知会替换         | `"message_123"`                     |
| `ChannelID`   | string                        | 通知渠道 ID（Android 8.0+）            | `"important_channel"`               |
| `Priority`    | AndroidNotificationPriority   | 通知优先级（MIN/LOW/DEFAULT/HIGH/MAX） | `PriorityHigh`                      |
| `Visibility`  | AndroidNotificationVisibility | 锁屏显示模式（PRIVATE/PUBLIC/SECRET）  | `VisibilityPrivate`                 |
| `ClickAction` | string                        | 点击通知时的动作                       | `"OPEN_ACTIVITY"`                   |

### 2. iOS 配置 (`APNSConfig`)

#### 主要字段

| 字段                | 类型              | 说明                           | 示例                      |
|---------------------|-------------------|--------------------------------|---------------------------|
| `Headers`           | map[string]string | APNs HTTP/2 头信息             | `{"apns-priority": "10"}` |
| `Payload`           | *APNSPayload      | APNs 负载内容                  | 见下表                    |
| `FCMOptions`        | *APNSFCMOptions   | FCM 特定选项                   | -                         |
| `LiveActivityToken` | string            | Live Activity token（iOS 16+） | -                         |

#### APNSPayload.Aps 主要字段

| 字段               | 类型      | 说明                         | 示例                                |
|--------------------|-----------|------------------------------|-------------------------------------|
| `Badge`            | *int      | 应用角标数字                 | `&5`                                |
| `Sound`            | string    | 通知声音                     | `"default"` 或 `"notification.wav"` |
| `Alert`            | *ApsAlert | 通知内容（可定制标题和内容） | -                                   |
| `Category`         | string    | 通知类别（用于操作按钮）     | `"MESSAGE_CATEGORY"`                |
| `ContentAvailable` | bool      | 是否触发后台应用刷新         | `true`                              |
| `MutableContent`   | bool      | 是否允许通知扩展修改         | `true`                              |
| `ThreadID`         | string    | 通知线程 ID（用于分组）      | `"conversation_123"`                |

#### 常用 Headers

| Header            | 值                          | 说明                       |
|-------------------|-----------------------------|----------------------------|
| `apns-priority`   | `"10"` 或 `"5"`             | 优先级（10=立即，5=省电）  |
| `apns-expiration` | `"0"` 或 Unix 时间戳        | 消息过期时间               |
| `apns-push-type`  | `"alert"` 或 `"background"` | 推送类型                   |
| `apns-topic`      | Bundle ID                   | 应用标识符（通常自动设置） |

### 3. Web 配置 (`WebpushConfig`)

#### 主要字段

| 字段           | 类型                 | 说明               | 示例   |
|----------------|----------------------|--------------------|--------|
| `Headers`      | map[string]string    | WebPush 协议头信息 | -      |
| `Notification` | *WebpushNotification | Web 通知特定配置   | 见下表 |
| `FCMOptions`   | *WebpushFCMOptions   | FCM 特定选项       | -      |

#### WebpushNotification 主要字段

| 字段                 | 类型                         | 说明                         | 示例                              |
|----------------------|------------------------------|------------------------------|-----------------------------------|
| `Title`              | string                       | 通知标题（覆盖通用标题）     | `"新消息"`                        |
| `Body`               | string                       | 通知内容（覆盖通用内容）     | `"您有一条新消息"`                |
| `Icon`               | string                       | 通知图标 URL                 | `"https://example.com/icon.png"`  |
| `Badge`              | string                       | 徽章图标 URL                 | `"https://example.com/badge.png"` |
| `Image`              | string                       | 通知大图 URL                 | `"https://example.com/image.jpg"` |
| `Tag`                | string                       | 通知标签（相同标签会替换）   | `"message_123"`                   |
| `Actions`            | []*WebpushNotificationAction | 操作按钮                     | 见下表                            |
| `RequireInteraction` | bool                         | 是否需要用户交互才能关闭     | `true`                            |
| `Silent`             | bool                         | 是否静默通知（不显示）       | `false`                           |
| `Renotify`           | bool                         | 相同标签的新通知是否重新提醒 | `true`                            |

#### WebpushNotificationAction

| 字段     | 类型   | 说明         | 示例                                  |
|----------|--------|--------------|---------------------------------------|
| `Action` | string | 操作标识符   | `"view"`                              |
| `Title`  | string | 按钮显示文本 | `"查看"`                              |
| `Icon`   | string | 按钮图标 URL | `"https://example.com/view-icon.png"` |

## 五、实际使用示例

### 示例 1: 完整的平台特定配置

```go
func (c *Client) SendPlatformSpecificMessage(token string, msg *Message) error {
    ctx := context.Background()
    
    // 基础通知（所有平台通用）
    notification := &messaging.Notification{
        Title: msg.Title,
        Body:  msg.Body,
    }
    
    if msg.Image != "" {
        notification.ImageURL = msg.Image
    }
    
    // Android 配置
    androidConfig := &messaging.AndroidConfig{
        Priority: "high",
        Notification: &messaging.AndroidNotification{
            Icon:  "notification_icon",
            Color: "#2196F3",
            Sound: "default",
            ChannelID: "default_channel",
        },
    }
    
    // iOS 配置
    badgeCount := 1
    apnsConfig := &messaging.APNSConfig{
        Headers: map[string]string{
            "apns-priority": "10",
        },
        Payload: &messaging.APNSPayload{
            Aps: &messaging.Aps{
                Badge: &badgeCount,
                Sound: "default",
                ContentAvailable: true,
            },
        },
    }
    
    // Web 配置
    webpushConfig := &messaging.WebpushConfig{
        Notification: &messaging.WebpushNotification{
            Icon: "https://example.com/icon.png",
            Actions: []*messaging.WebpushNotificationAction{
                {Action: "view", Title: "查看"},
                {Action: "dismiss", Title: "忽略"},
            },
        },
        FCMOptions: &messaging.WebpushFCMOptions{
            Link: "https://example.com/notification",
        },
    }
    
    // 构建消息
    message := &messaging.Message{
        Token:        token,
        Notification: notification,
        Data:         msg.Data,
        Android:      androidConfig,
        APNS:         apnsConfig,
        Webpush:      webpushConfig,
    }
    
    response, err := c.messaging.Send(ctx, message)
    if err != nil {
        return fmt.Errorf("发送推送失败: %w", err)
    }
    
    log.Printf("推送成功发送: %s", response)
    return nil
}
```

### 示例 2: 根据平台动态配置

```go
func (c *Client) SendToPlatform(token string, platform string, msg *Message) error {
    ctx := context.Background()
    
    notification := &messaging.Notification{
        Title: msg.Title,
        Body:  msg.Body,
    }
    
    message := &messaging.Message{
        Token:        token,
        Notification: notification,
        Data:         msg.Data,
    }
    
    // 根据平台添加特定配置
    switch platform {
    case "android":
        message.Android = &messaging.AndroidConfig{
            Priority: "high",
            Notification: &messaging.AndroidNotification{
                Icon:  "app_icon",
                Color: "#4CAF50",
            },
        }
    case "ios":
        badgeCount := 1
        message.APNS = &messaging.APNSConfig{
            Payload: &messaging.APNSPayload{
                Aps: &messaging.Aps{
                    Badge: &badgeCount,
                },
            },
        }
    case "web":
        message.Webpush = &messaging.WebpushConfig{
            Notification: &messaging.WebpushNotification{
                Icon: "https://example.com/web-icon.png",
            },
        }
    }
    
    response, err := c.messaging.Send(ctx, message)
    if err != nil {
        return fmt.Errorf("发送推送失败: %w", err)
    }
    
    log.Printf("推送成功发送: %s", response)
    return nil
}
```

### 示例 3: 高优先级 Android 推送

```go
func (c *Client) SendHighPriorityAndroidPush(token string, msg *Message) error {
    ctx := context.Background()
    
    ttl := 24 * time.Hour
    message := &messaging.Message{
        Token: token,
        Notification: &messaging.Notification{
            Title: msg.Title,
            Body:  msg.Body,
        },
        Android: &messaging.AndroidConfig{
            Priority: "high",  // 高优先级
            TTL:      &ttl,     // 24 小时过期
            CollapseKey: "important_update",
            Notification: &messaging.AndroidNotification{
                Icon:      "important_icon",
                Color:     "#FF0000",  // 红色
                Sound:     "alert.wav",
                ChannelID: "critical_channel",
                Priority:  messaging.PriorityMax,  // 最高通知优先级
                Visibility: messaging.VisibilityPublic,
            },
        },
    }
    
    response, err := c.messaging.Send(ctx, message)
    if err != nil {
        return fmt.Errorf("发送推送失败: %w", err)
    }
    
    log.Printf("高优先级推送发送成功: %s", response)
    return nil
}
```

### 示例 4: iOS 后台静默推送

```go
func (c *Client) SendSilentBackgroundPush(token string, data map[string]string) error {
    ctx := context.Background()
    
    message := &messaging.Message{
        Token: token,
        Data:  data,
        APNS: &messaging.APNSConfig{
            Headers: map[string]string{
                "apns-priority": "5",        // 低优先级（省电）
                "apns-push-type": "background",
            },
            Payload: &messaging.APNSPayload{
                Aps: &messaging.Aps{
                    ContentAvailable: true,  // 触发后台应用刷新
                },
            },
        },
    }
    
    response, err := c.messaging.Send(ctx, message)
    if err != nil {
        return fmt.Errorf("发送静默推送失败: %w", err)
    }
    
    log.Printf("静默推送发送成功: %s", response)
    return nil
}
```

## 六、总结

### 当前代码的优势

✅ **简单易用** - 不需要了解各平台的复杂配置  
✅ **跨平台统一** - 一个代码路径支持所有平台  
✅ **快速开发** - 适合大多数基本推送需求  

### 使用平台特定配置的优势

✅ **精细控制** - 可以为每个平台定制推送行为  
✅ **更好的用户体验** - 利用各平台的特性（图标、颜色、优先级等）  
✅ **功能丰富** - 支持高级特性（操作按钮、后台更新、静默推送等）  

### 建议

| 场景                    | 推荐方案                               |
|-------------------------|----------------------------------------|
| **基本推送需求**        | 使用当前代码（通用配置）               |
| **需要平台特定样式**    | 添加 `Android`、`APNS`、`Webpush` 配置 |
| **多平台应用**          | 使用通用配置 + 按需添加平台特定配置    |
| **高性能/高优先级推送** | 必须使用平台特定配置                   |

### 迁移建议

如果你需要平台特定功能，可以：

1. **保持向后兼容** - 在现有方法中添加可选参数
2. **新增方法** - 创建专门的方法处理平台特定配置
3. **扩展 Message 结构** - 在自定义 `Message` 中添加平台配置字段

例如：

```go
// 扩展自定义 Message 结构
type Message struct {
    Title  string
    Body   string
    Image  string
    Data   map[string]string
    
    // 新增平台特定配置
    AndroidConfig *PlatformAndroidConfig
    APNSConfig    *PlatformAPNSConfig
    WebpushConfig *PlatformWebpushConfig
}
```

这样可以逐步迁移，不需要一次性重写所有代码。


