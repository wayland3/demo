# Firebase Cloud Messaging (FCM) 接入步骤

## 步骤一：在 Firebase Console 创建项目

1. 访问 [Firebase Console](https://console.firebase.google.com/)
2. 点击"添加项目"或选择现有项目
3. 按照向导完成项目创建

## 步骤二：创建服务账号并获取密钥文件

1. 在 Firebase 项目中，进入 **项目设置** > **服务账号**
2. 点击 **生成新的私钥** 按钮
3. 下载生成的 JSON 密钥文件（例如：`service-account-key.json`）
4. **重要**：妥善保管此文件，不要提交到版本控制系统

## 步骤三：在 Go 项目中安装依赖

```bash
go get firebase.google.com/go/v4
go get google.golang.org/api/option
```

## 步骤四：实现 FCM 客户端

参考 `fcm_client.go` 文件中的实现。

## 步骤五：配置环境变量

将服务账号密钥文件路径设置为环境变量：

```bash
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/service-account-key.json"
```

或者直接在代码中指定密钥文件路径。

## 步骤六：使用示例

```go
// 初始化 FCM 客户端
client, err := NewFCMClient("path/to/service-account-key.json")
if err != nil {
    log.Fatal(err)
}

// 发送单设备推送
err = client.SendToDevice("device-fcm-token", &Message{
    Title: "标题",
    Body:  "消息内容",
    Data:  map[string]string{"key": "value"},
})

// 发送多设备推送
tokens := []string{"token1", "token2", "token3"}
err = client.SendToMultipleDevices(tokens, &Message{
    Title: "批量推送",
    Body:  "这是批量推送消息",
})

// 发送主题推送
err = client.SendToTopic("news", &Message{
    Title: "新闻推送",
    Body:  "今日新闻",
})
```

## 步骤七：客户端获取 FCM Token

### Android
1. 在 `build.gradle` 中添加 Firebase 依赖
2. 在应用初始化时获取 FCM Token
3. 将 Token 发送到后端服务器保存

### iOS
1. 在 Xcode 项目中集成 Firebase SDK
2. 配置 APNs 证书
3. 获取 FCM Token 并发送到后端

## 注意事项

1. **安全性**：服务账号密钥文件包含敏感信息，不要提交到 Git
2. **Token 管理**：FCM Token 可能会变化，需要定期更新
3. **配额限制**：注意 Firebase 的推送配额限制
4. **错误处理**：处理无效 Token、网络错误等情况
5. **测试环境**：建议先在测试环境验证功能


