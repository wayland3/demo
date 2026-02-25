# option.ClientOption 可用选项详解

本文档列出了所有可以传入 `firebase.NewApp()` 或 `NewFCMClient()` 的 `option.ClientOption` 选项。

## 一、认证相关选项

### 1. WithCredentialsFile

使用服务账号密钥文件进行认证（最常用）。

```go
import "google.golang.org/api/option"

opts := []option.ClientOption{
    option.WithCredentialsFile("./service-account-key.json"),
}
```

**说明**:
- 传入服务账号密钥文件的路径
- 这是最常用的认证方式
- 对应环境变量：`GOOGLE_APPLICATION_CREDENTIALS`

### 2. WithCredentialsJSON

使用服务账号密钥 JSON 内容（字节数组）进行认证。

```go
import (
    "google.golang.org/api/option"
    "io/ioutil"
)

jsonData, _ := ioutil.ReadFile("./service-account-key.json")
opts := []option.ClientOption{
    option.WithCredentialsJSON(jsonData),
}
```

**说明**:
- 直接传入 JSON 字节数组
- 适用于从数据库或其他存储读取密钥的场景
- ⚠️ 注意安全性，不要将密钥暴露在代码中

### 3. WithTokenSource

使用 OAuth2 Token Source 进行认证。

```go
import (
    "golang.org/x/oauth2"
    "golang.org/x/oauth2/google"
    "google.golang.org/api/option"
)

ts, _ := google.DefaultTokenSource(ctx, "https://www.googleapis.com/auth/firebase.messaging")
opts := []option.ClientOption{
    option.WithTokenSource(ts),
}
```

**说明**:
- 适用于需要使用自定义 Token Source 的场景
- 需要指定正确的 OAuth2 作用域（scopes）

### 4. WithCredentials

使用 `google.Credentials` 对象进行认证。

```go
import (
    "golang.org/x/oauth2/google"
    "google.golang.org/api/option"
)

creds, _ := google.FindDefaultCredentials(ctx, "https://www.googleapis.com/auth/firebase.messaging")
opts := []option.ClientOption{
    option.WithCredentials(creds),
}
```

### 5. WithAuthCredentials

使用新的认证库 `cloud.google.com/go/auth.Credentials`（实验性）。

```go
import (
    "cloud.google.com/go/auth"
    "google.golang.org/api/option"
)

creds := &auth.Credentials{...}
opts := []option.ClientOption{
    option.WithAuthCredentials(creds),
}
```

### 6. WithAPIKey

使用 API Key 进行认证（仅限 JSON-over-HTTP API）。

```go
opts := []option.ClientOption{
    option.WithAPIKey("your-api-key"),
}
```

**说明**:
- ⚠️ 仅适用于某些 Google API，Firebase 推送通常不使用 API Key
- 适用于不需要服务账号的场景

### 7. WithoutAuthentication

不使用认证（仅用于测试或访问公开资源）。

```go
opts := []option.ClientOption{
    option.WithoutAuthentication(),
}
```

**说明**:
- ⚠️ 仅用于测试或访问公开资源
- 不能与其他认证选项同时使用

## 二、OAuth2 作用域选项

### 8. WithScopes

指定 OAuth2 作用域。

```go
opts := []option.ClientOption{
    option.WithScopes(
        "https://www.googleapis.com/auth/firebase.messaging",
        "https://www.googleapis.com/auth/cloud-platform",
    ),
}
```

**常用作用域**:
- `https://www.googleapis.com/auth/firebase.messaging` - Firebase 推送服务
- `https://www.googleapis.com/auth/cloud-platform` - 完整的 Google Cloud Platform 访问

## 三、HTTP 客户端选项

### 9. WithHTTPClient

使用自定义的 HTTP 客户端。

```go
import (
    "net/http"
    "time"
    "google.golang.org/api/option"
)

customClient := &http.Client{
    Timeout: 30 * time.Second,
    Transport: &http.Transport{
        MaxIdleConns:       100,
        IdleConnTimeout:    90 * time.Second,
        DisableCompression: false,
    },
}

opts := []option.ClientOption{
    option.WithHTTPClient(customClient),
}
```

**说明**:
- 可以自定义超时时间、连接池等
- 此选项会覆盖其他 HTTP 相关选项
- 与 `WithUserAgent` 不兼容

### 10. WithEndpoint

覆盖默认的服务端点 URL。

```go
opts := []option.ClientOption{
    option.WithEndpoint("https://fcm.googleapis.com/v1"),
}
```

**说明**:
- 默认端点是 `https://fcm.googleapis.com/v1`
- 通常不需要修改，除非使用自定义端点

### 11. WithUserAgent

设置自定义 User-Agent 头。

```go
opts := []option.ClientOption{
    option.WithUserAgent("MyApp/1.0"),
}
```

**说明**:
- 与 `WithHTTPClient` 不兼容
- 如果需要自定义 User-Agent，应该在 HTTP Client 的 RoundTripper 中设置

## 四、日志和监控选项

### 12. WithLogger

设置自定义日志记录器。

```go
import (
    "log/slog"
    "google.golang.org/api/option"
)

logger := slog.New(slog.NewJSONHandler(os.Stdout, nil))
opts := []option.ClientOption{
    option.WithLogger(logger),
}
```

**说明**:
- 使用 Go 1.21+ 的 `slog` 包
- 可以自定义日志格式和输出位置

### 13. WithTelemetryDisabled

禁用默认的遥测功能（OpenCensus）。

```go
opts := []option.ClientOption{
    option.WithTelemetryDisabled(),
}
```

**说明**:
- 禁用后可以使用自定义的遥测实现
- 适用于需要绑定自定义监控的场景

## 五、配额和计费选项

### 14. WithQuotaProject

指定用于配额和计费的项目 ID。

```go
opts := []option.ClientOption{
    option.WithQuotaProject("my-quota-project-id"),
}
```

**说明**:
- 当使用的服务账号不属于当前项目时有用
- 用于配额限制和计费追踪

### 15. WithRequestReason

设置请求原因（用于审计日志）。

```go
opts := []option.ClientOption{
    option.WithRequestReason("support-case-12345"),
}
```

**说明**:
- 例如：支持工单号、任务 ID 等
- 会记录在审计日志中，便于追踪

## 六、TLS/SSL 选项

### 16. WithClientCertSource

指定 TLS 客户端证书源（用于 mTLS 认证）。

```go
import (
    "crypto/tls"
    "google.golang.org/api/option"
)

certSource := func(info *tls.CertificateRequestInfo) (*tls.Certificate, error) {
    // 返回客户端证书
    cert, err := tls.LoadX509KeyPair("client.crt", "client.key")
    return &cert, err
}

opts := []option.ClientOption{
    option.WithClientCertSource(certSource),
}
```

**说明**:
- 用于双向 TLS (mTLS) 认证
- 服务器会验证客户端证书
- 这是实验性 API，可能会变化

## 七、域名和身份选项

### 17. WithUniverseDomain

设置 Universe Domain（企业版 Google Cloud）。

```go
opts := []option.ClientOption{
    option.WithUniverseDomain("mycompany.com"),
}
```

**说明**:
- 仅用于企业版 Google Cloud
- 大多数用户不需要此选项

### 18. WithAudiences

指定 JWT Token 的受众（audience）。

```go
opts := []option.ClientOption{
    option.WithAudiences("https://fcm.googleapis.com/"),
}
```

**说明**:
- 用于 JWT Token 认证
- 指定 Token 的目标受众

## 八、服务账号模拟选项

### 19. ImpersonateCredentials

模拟目标服务账号（已废弃）。

```go
// ⚠️ 已废弃，不推荐使用
opts := []option.ClientOption{
    option.ImpersonateCredentials("target-service-account@project.iam.gserviceaccount.com"),
}
```

**说明**:
- ⚠️ 此选项已废弃
- 推荐使用 `impersonate` 包：`google.golang.org/api/impersonate`
- 配合 `WithTokenSource` 使用

## 九、完整示例

### 示例 1: 基本使用（推荐）

```go
import (
    "context"
    "google.golang.org/api/option"
    firebase "firebase.google.com/go/v4"
)

func NewFCMClient(credentialsPath string) (*FCMClient, error) {
    ctx := context.Background()
    
    opts := []option.ClientOption{
        option.WithCredentialsFile(credentialsPath),
    }
    
    app, err := firebase.NewApp(ctx, nil, opts...)
    if err != nil {
        return nil, err
    }
    
    // ...
}
```

### 示例 2: 使用自定义 HTTP 客户端

```go
import (
    "net/http"
    "time"
    "google.golang.org/api/option"
)

func NewFCMClientWithCustomHTTP(credentialsPath string) (*FCMClient, error) {
    ctx := context.Background()
    
    // 自定义 HTTP 客户端
    httpClient := &http.Client{
        Timeout: 60 * time.Second,
        Transport: &http.Transport{
            MaxIdleConns:        100,
            MaxIdleConnsPerHost: 10,
            IdleConnTimeout:     90 * time.Second,
        },
    }
    
    opts := []option.ClientOption{
        option.WithCredentialsFile(credentialsPath),
        option.WithHTTPClient(httpClient),
    }
    
    app, err := firebase.NewApp(ctx, nil, opts...)
    // ...
}
```

### 示例 3: 使用日志记录器

```go
import (
    "log/slog"
    "os"
    "google.golang.org/api/option"
)

func NewFCMClientWithLogger(credentialsPath string) (*FCMClient, error) {
    ctx := context.Background()
    
    // 创建 JSON 格式的日志记录器
    logger := slog.New(slog.NewJSONHandler(os.Stdout, &slog.HandlerOptions{
        Level: slog.LevelInfo,
    }))
    
    opts := []option.ClientOption{
        option.WithCredentialsFile(credentialsPath),
        option.WithLogger(logger),
    }
    
    app, err := firebase.NewApp(ctx, nil, opts...)
    // ...
}
```

### 示例 4: 使用 JSON 密钥内容

```go
import (
    "encoding/json"
    "io/ioutil"
    "google.golang.org/api/option"
)

func NewFCMClientFromJSON(jsonPath string) (*FCMClient, error) {
    ctx := context.Background()
    
    // 从文件读取 JSON
    jsonData, err := ioutil.ReadFile(jsonPath)
    if err != nil {
        return nil, err
    }
    
    // 可选：验证 JSON 格式
    var creds map[string]interface{}
    if err := json.Unmarshal(jsonData, &creds); err != nil {
        return nil, fmt.Errorf("无效的 JSON 格式: %w", err)
    }
    
    opts := []option.ClientOption{
        option.WithCredentialsJSON(jsonData),
    }
    
    app, err := firebase.NewApp(ctx, nil, opts...)
    // ...
}
```

### 示例 5: 组合多个选项

```go
func NewFCMClientWithMultipleOptions(credentialsPath string) (*FCMClient, error) {
    ctx := context.Background()
    
    logger := slog.New(slog.NewJSONHandler(os.Stdout, nil))
    
    opts := []option.ClientOption{
        option.WithCredentialsFile(credentialsPath),
        option.WithScopes("https://www.googleapis.com/auth/firebase.messaging"),
        option.WithLogger(logger),
        option.WithQuotaProject("my-quota-project"),
        option.WithRequestReason("batch-push-2024-01-01"),
    }
    
    app, err := firebase.NewApp(ctx, nil, opts...)
    // ...
}
```

## 十、选项优先级和兼容性

### 选项优先级

1. `WithHTTPClient` - 如果设置，会覆盖其他 HTTP 相关选项
2. `WithGRPCConn` - 如果设置，会覆盖其他 gRPC 相关选项
3. 认证选项 - 只能使用一个：
   - `WithCredentialsFile`
   - `WithCredentialsJSON`
   - `WithTokenSource`
   - `WithCredentials`
   - `WithAPIKey`
   - `WithoutAuthentication`

### 不兼容的组合

- ❌ `WithHTTPClient` + `WithUserAgent` - 不兼容
- ❌ 多个认证选项同时使用 - 只能使用一个
- ❌ `WithoutAuthentication` + 任何认证选项

## 十一、常用场景推荐

### 场景 1: 生产环境（推荐）

```go
opts := []option.ClientOption{
    option.WithCredentialsFile(os.Getenv("GOOGLE_APPLICATION_CREDENTIALS")),
}
```

### 场景 2: 需要自定义超时

```go
httpClient := &http.Client{
    Timeout: 30 * time.Second,
}

opts := []option.ClientOption{
    option.WithCredentialsFile(credentialsPath),
    option.WithHTTPClient(httpClient),
}
```

### 场景 3: 需要日志记录

```go
logger := slog.New(slog.NewJSONHandler(os.Stdout, nil))

opts := []option.ClientOption{
    option.WithCredentialsFile(credentialsPath),
    option.WithLogger(logger),
}
```

### 场景 4: 从环境变量或配置读取密钥

```go
var opts []option.ClientOption

if jsonPath := os.Getenv("GOOGLE_APPLICATION_CREDENTIALS"); jsonPath != "" {
    opts = append(opts, option.WithCredentialsFile(jsonPath))
} else if jsonData := os.Getenv("GOOGLE_APPLICATION_CREDENTIALS_JSON"); jsonData != "" {
    opts = append(opts, option.WithCredentialsJSON([]byte(jsonData)))
}
```

## 十二、总结

### 最常用的选项

1. ✅ **WithCredentialsFile** - 文件路径认证（最常用）
2. ✅ **WithCredentialsJSON** - JSON 内容认证
3. ✅ **WithHTTPClient** - 自定义 HTTP 客户端
4. ✅ **WithLogger** - 日志记录

### 较少使用的选项

- `WithScopes` - 通常使用默认作用域即可
- `WithEndpoint` - 通常使用默认端点即可
- `WithQuotaProject` - 特殊场景使用
- `WithRequestReason` - 需要审计追踪时使用

### 参考文档

- Google API Go Client 文档: https://pkg.go.dev/google.golang.org/api/option
- Firebase Admin Go SDK 文档: https://pkg.go.dev/firebase.google.com/go/v4

