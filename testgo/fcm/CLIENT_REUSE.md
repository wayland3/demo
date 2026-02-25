# FCM 客户端复用最佳实践

## 一、核心答案

**是的，FCM Client 应该创建一次，然后在应用生命周期内持续复用。**

## 二、为什么应该复用 Client？

### 1. 性能优势

- ✅ **减少初始化开销**：创建 Firebase App 和 Messaging Client 需要加载配置、建立连接等操作
- ✅ **复用连接**：底层 HTTP 连接可以被复用，减少网络开销
- ✅ **降低内存占用**：多个 Client 实例会占用更多内存

### 2. 线程安全

Firebase Go SDK 的 `messaging.Client` 是**线程安全的**，可以在多个 goroutine 中安全地并发使用。

### 3. 资源管理

- ✅ 统一管理 Firebase 应用实例
- ✅ 更好的资源控制和清理

## 三、正确的使用方式

### 方式 1：全局单例（推荐）

在应用启动时创建一次，整个应用生命周期内复用：

```go
package fcm

import (
    "sync"
    "firebase.google.com/go/v4"
    "firebase.google.com/go/v4/messaging"
)

var (
    clientInstance *FCMClient
    clientOnce     sync.Once
    clientError    error
)

// GetFCMClient 获取 FCM 客户端单例
func GetFCMClient(credentialsPath string) (*FCMClient, error) {
    clientOnce.Do(func() {
        clientInstance, clientError = NewFCMClient(credentialsPath)
    })
    return clientInstance, clientError
}
```

### 方式 2：作为服务的一部分

在服务初始化时创建，作为服务的一部分：

```go
type PushService struct {
    fcmClient *fcm.FCMClient
    // ... 其他字段
}

func NewPushService(credentialsPath string) (*PushService, error) {
    client, err := fcm.NewFCMClient(credentialsPath)
    if err != nil {
        return nil, err
    }
    
    return &PushService{
        fcmClient: client,
    }, nil
}

func (s *PushService) SendPush(token string, msg *fcm.Message) error {
    return s.fcmClient.SendToDevice(token, msg)
}
```

### 方式 3：依赖注入

如果使用依赖注入框架（如 Wire），可以通过依赖注入管理：

```go
// wire.go
func InitializePushService(credentialsPath string) (*PushService, error) {
    wire.Build(
        fcm.NewFCMClient,
        NewPushService,
    )
    return nil, nil
}
```

## 四、Web 服务中的使用示例

### HTTP 服务示例

```go
package main

import (
    "log"
    "net/http"
    "os"
    "sync"
    
    "ttt/fcm"
)

// PushService 推送服务
type PushService struct {
    client *fcm.FCMClient
    mu     sync.RWMutex
}

var pushService *PushService
var pushServiceOnce sync.Once

// GetPushService 获取推送服务单例
func GetPushService() (*PushService, error) {
    var err error
    pushServiceOnce.Do(func() {
        credentialsPath := os.Getenv("GOOGLE_APPLICATION_CREDENTIALS")
        if credentialsPath == "" {
            credentialsPath = "./service-account-key.json"
        }
        
        client, e := fcm.NewFCMClient(credentialsPath)
        if e != nil {
            err = e
            return
        }
        
        pushService = &PushService{
            client: client,
        }
    })
    return pushService, err
}

// SendPush HTTP 处理函数
func sendPushHandler(w http.ResponseWriter, r *http.Request) {
    service, err := GetPushService()
    if err != nil {
        http.Error(w, "推送服务初始化失败", http.StatusInternalServerError)
        return
    }
    
    // 使用复用的 client 发送推送
    token := r.URL.Query().Get("token")
    err = service.client.SendToDevice(token, &fcm.Message{
        Title: "测试推送",
        Body:  "这是一条测试消息",
    })
    
    if err != nil {
        http.Error(w, err.Error(), http.StatusInternalServerError)
        return
    }
    
    w.WriteHeader(http.StatusOK)
    w.Write([]byte("推送发送成功"))
}

func main() {
    // 初始化推送服务（只执行一次）
    _, err := GetPushService()
    if err != nil {
        log.Fatalf("初始化推送服务失败: %v", err)
    }
    
    // 注册路由
    http.HandleFunc("/push", sendPushHandler)
    
    // 启动服务
    log.Println("服务器启动在 :8080")
    log.Fatal(http.ListenAndServe(":8080", nil))
}
```

### 并发使用示例

```go
// 多个 goroutine 可以安全地使用同一个 client
func sendBatchPushes(tokens []string, msg *fcm.Message) {
    service, _ := GetPushService()
    
    // 并发发送推送（使用同一个 client）
    var wg sync.WaitGroup
    for _, token := range tokens {
        wg.Add(1)
        go func(t string) {
            defer wg.Done()
            // 线程安全，可以并发调用
            service.client.SendToDevice(t, msg)
        }(token)
    }
    wg.Wait()
}
```

## 五、错误的使用方式

### ❌ 每次发送都创建新 Client

```go
func sendPushBad(token string) error {
    // ❌ 错误：每次都创建新 client，性能差
    client, err := fcm.NewFCMClient("./service-account-key.json")
    if err != nil {
        return err
    }
    return client.SendToDevice(token, &fcm.Message{
        Title: "标题",
        Body:  "内容",
    })
}
```

**问题**：
- 每次调用都要初始化 Firebase App
- 浪费资源，性能差
- 可能导致连接数过多

### ❌ 不检查错误就复用

```go
var globalClient *fcm.FCMClient

func init() {
    // ❌ 错误：如果初始化失败，globalClient 可能是 nil
    globalClient, _ = fcm.NewFCMClient("./service-account-key.json")
}
```

## 六、客户端生命周期管理

### 应用启动时初始化

```go
type App struct {
    fcmClient *fcm.FCMClient
    // ... 其他服务
}

func NewApp() (*App, error) {
    // 应用启动时初始化一次
    fcmClient, err := fcm.NewFCMClient(os.Getenv("GOOGLE_APPLICATION_CREDENTIALS"))
    if err != nil {
        return nil, fmt.Errorf("初始化 FCM 客户端失败: %w", err)
    }
    
    return &App{
        fcmClient: fcmClient,
    }, nil
}

func (app *App) Shutdown() {
    // 应用关闭时的清理工作
    // FCM Client 通常不需要特殊清理，但可以在这里做其他清理
}
```

### 优雅关闭

虽然 FCM Client 不需要特殊清理，但如果需要，可以这样处理：

```go
type FCMClientWrapper struct {
    client *fcm.FCMClient
    ctx    context.Context
    cancel context.CancelFunc
}

func NewFCMClientWrapper(credentialsPath string) (*FCMClientWrapper, error) {
    ctx, cancel := context.WithCancel(context.Background())
    
    client, err := fcm.NewFCMClient(credentialsPath)
    if err != nil {
        cancel()
        return nil, err
    }
    
    return &FCMClientWrapper{
        client: client,
        ctx:    ctx,
        cancel: cancel,
    }, nil
}

func (w *FCMClientWrapper) Close() {
    w.cancel()
    // 可以在这里做其他清理工作
}
```

## 七、完整的单例实现示例

创建一个改进的客户端管理器：

```go
package fcm

import (
    "context"
    "sync"
    "fmt"
    
    firebase "firebase.google.com/go/v4"
    "firebase.google.com/go/v4/messaging"
    "google.golang.org/api/option"
)

// ClientManager FCM 客户端管理器
type ClientManager struct {
    client *FCMClient
    mu     sync.RWMutex
}

var (
    defaultManager *ClientManager
    defaultManagerOnce sync.Once
)

// InitDefaultClient 初始化默认客户端（应用启动时调用一次）
func InitDefaultClient(credentialsPath string) error {
    var err error
    defaultManagerOnce.Do(func() {
        client, e := NewFCMClient(credentialsPath)
        if e != nil {
            err = e
            return
        }
        defaultManager = &ClientManager{
            client: client,
        }
    })
    return err
}

// GetDefaultClient 获取默认客户端（线程安全）
func GetDefaultClient() (*FCMClient, error) {
    if defaultManager == nil {
        return nil, fmt.Errorf("FCM 客户端未初始化，请先调用 InitDefaultClient")
    }
    defaultManager.mu.RLock()
    defer defaultManager.mu.RUnlock()
    return defaultManager.client, nil
}

// MustGetDefaultClient 获取默认客户端，如果未初始化则 panic
func MustGetDefaultClient() *FCMClient {
    client, err := GetDefaultClient()
    if err != nil {
        panic(err)
    }
    return client
}
```

使用示例：

```go
package main

import (
    "log"
    "os"
    "ttt/fcm"
)

func main() {
    // 应用启动时初始化一次
    credentialsPath := os.Getenv("GOOGLE_APPLICATION_CREDENTIALS")
    if err := fcm.InitDefaultClient(credentialsPath); err != nil {
        log.Fatalf("初始化 FCM 客户端失败: %v", err)
    }
    
    // 任何地方都可以安全地获取客户端
    client, err := fcm.GetDefaultClient()
    if err != nil {
        log.Fatal(err)
    }
    
    // 使用客户端发送推送
    err = client.SendToDevice("token", &fcm.Message{
        Title: "标题",
        Body:  "内容",
    })
    
    // 或者使用 MustGet（如果确定已初始化）
    client2 := fcm.MustGetDefaultClient()
    client2.SendToDevice("token", &fcm.Message{
        Title: "标题",
        Body:  "内容",
    })
}
```

## 八、最佳实践总结

### ✅ 应该做的

1. **应用启动时创建一次**
   ```go
   // 在 main() 或服务初始化时
   client, err := fcm.NewFCMClient(credentialsPath)
   ```

2. **在整个应用生命周期内复用**
   ```go
   // 保存为全局变量、单例或服务的一部分
   type Service struct {
       fcmClient *fcm.FCMClient
   }
   ```

3. **线程安全使用**
   ```go
   // 可以在多个 goroutine 中并发使用
   go client.SendToDevice(token1, msg)
   go client.SendToDevice(token2, msg)
   ```

4. **错误处理**
   ```go
   // 初始化失败时应该处理错误
   client, err := fcm.NewFCMClient(credentialsPath)
   if err != nil {
       log.Fatal(err)
   }
   ```

### ❌ 不应该做的

1. ❌ **每次发送都创建新 Client**
2. ❌ **在循环中创建 Client**
3. ❌ **忽略初始化错误**

## 九、性能对比

| 方式        | 初始化时间     | 内存占用 | 网络开销 | 推荐度 |
|-------------|----------------|----------|----------|--------|
| 复用 Client | 一次（~100ms） | 低       | 低       | ⭐⭐⭐⭐⭐  |
| 每次创建    | 每次（~100ms） | 高       | 高       | ⭐      |

## 十、总结

**FCM Client 应该：**
- ✅ 在应用启动时创建一次
- ✅ 作为单例或服务的一部分保存
- ✅ 在整个应用生命周期内复用
- ✅ 可以在多个 goroutine 中并发使用（线程安全）

**核心原则：创建一次，复用多次。**


