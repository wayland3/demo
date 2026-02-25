# AppCheck 详解

## 一、AppCheck 是什么？

**Firebase App Check** 是 Firebase 提供的一项安全服务，用于保护后端资源免受滥用。它验证来自合法应用的请求。

### 核心概念

- **客户端（移动应用）**：生成 App Check Token
- **后端服务器**：验证 App Check Token，确认请求来自合法应用

## 二、`app.AppCheck(ctx)` 的作用

### 方法签名

```go
func (a *App) AppCheck(ctx context.Context) (*appcheck.Client, error)
```

### 功能说明

这个方法返回一个 `appcheck.Client`，用于**验证客户端发送的 App Check Token**。

### 关键点

1. ✅ **会访问 Firebase 服务器**
   - 初始化时会从 Firebase 服务器下载 JWKS（JSON Web Key Set）
   - URL: `https://firebaseappcheck.googleapis.com/v1beta/jwks`

2. ✅ **用于验证 Token，不是生成 Token**
   - App Check Token 是在**客户端应用**中生成的
   - 后端服务器使用 `appcheck.Client` 来验证这些 Token

## 三、AppCheck 的初始化过程

### 源码分析

```75:89:firebase.google.com/go/v4@v4.18.0/appcheck/appcheck.go
func NewClient(ctx context.Context, conf *internal.AppCheckConfig) (*Client, error) {
	// TODO: Add support for overriding the HTTP client using the App one.
	jwks, err := keyfunc.Get(JWKSUrl, keyfunc.Options{
		Ctx:             ctx,
		RefreshInterval: 6 * time.Hour,
	})
	if err != nil {
		return nil, err
	}

	return &Client{
		projectID: conf.ProjectID,
		jwks:      jwks,
	}, nil
}
```

**关键信息**:
- ✅ 会访问 `https://firebaseappcheck.googleapis.com/v1beta/jwks`
- ✅ 下载 JWKS 用于验证 App Check Token
- ✅ JWKS 会每 6 小时自动刷新

### 网络请求

```
app.AppCheck(ctx)
    ↓
调用 NewClient()
    ↓
访问 Firebase 服务器
    ↓
GET https://firebaseappcheck.googleapis.com/v1beta/jwks
    ↓
下载 JWKS（公钥集合）
    ↓
用于后续验证 App Check Token
```

## 四、AppCheck 检查什么？

### VerifyToken 验证的内容

当后端收到客户端发送的 App Check Token 时，会验证：

```go
func (c *Client) VerifyToken(token string) (*DecodedAppCheckToken, error)
```

验证内容：

1. ✅ **Token 格式**
   - 必须是有效的 RS256 JWT
   - 必须包含正确的 header（typ: "JWT"）

2. ✅ **签名验证**
   - Token 必须由 Firebase App Check 服务器签名
   - 使用从 Firebase 下载的 JWKS 验证签名

3. ✅ **发行者（Issuer）**
   - `iss` 必须匹配：`https://firebaseappcheck.googleapis.com/`

4. ✅ **受众（Audience）**
   - `aud` 必须包含当前项目 ID：`projects/{project-id}`

5. ✅ **主体（Subject）**
   - `sub` 不能为空（通常是 App ID）

6. ✅ **过期时间**
   - Token 不能过期
   - Token 必须是最近颁发的

## 五、AppCheck 的使用场景

### 典型使用场景

```
移动应用（客户端）
    ↓
1. 生成 App Check Token
    ↓
2. 调用后端 API，携带 Token
    POST /api/your-endpoint
    Header: X-Firebase-AppCheck: <token>
    ↓
后端服务器
    ↓
3. 验证 App Check Token
    appcheckClient.VerifyToken(token)
    ↓
4. 验证通过 → 处理请求
   验证失败 → 拒绝请求
```

### 适用场景

- ✅ **保护 API 端点**：防止恶意请求
- ✅ **防止滥用**：确保请求来自合法的移动应用
- ✅ **增加安全性**：作为 API 密钥的补充

### 不适用场景

- ❌ **只发送推送通知**：FCM 推送不需要 App Check
- ❌ **服务器到服务器的通信**：App Check 只用于客户端验证

## 六、对于 FCM 推送的影响

### 关键结论

**对于只使用 FCM 推送的场景，`app.AppCheck(ctx)` 是不必要的。**

### 原因分析

1. ✅ **FCM 推送是服务器到服务器的通信**
   - 后端服务器 → Firebase 服务器 → 客户端设备
   - 不涉及客户端应用向后端发送请求

2. ✅ **FCM 已经有自己的认证机制**
   - 使用服务账号密钥文件认证
   - 不需要 App Check Token

3. ✅ **App Check 用于保护后端 API**
   - 验证客户端请求是否合法
   - FCM 推送场景下不需要

### 代码中的调用

在之前的代码中有这样一行：

```go
app, err := firebase.NewApp(ctx, nil, opts...)
app.AppCheck(ctx)  // ❌ 这行调用是不必要的
```

**这行代码的问题**:
- ❌ 会访问 Firebase 服务器下载 JWKS
- ❌ 但你永远不会使用返回的 `appcheck.Client`
- ❌ 浪费网络请求和资源
- ❌ 对于 FCM 推送没有任何作用

## 七、何时需要使用 AppCheck？

### 需要使用的场景

#### 场景 1: 保护后端 API

```go
// 后端 API 服务器
func handleAPIRequest(w http.ResponseWriter, r *http.Request) {
    // 从请求头获取 App Check Token
    token := r.Header.Get("X-Firebase-AppCheck")
    
    // 验证 Token
    appCheckClient, _ := app.AppCheck(ctx)
    decodedToken, err := appCheckClient.VerifyToken(token)
    if err != nil {
        http.Error(w, "Invalid App Check token", http.StatusUnauthorized)
        return
    }
    
    // Token 验证通过，处理请求
    // ...
}
```

#### 场景 2: 保护 Cloud Functions

```go
// Cloud Function 端点
func protectedFunction(w http.ResponseWriter, r *http.Request) {
    token := r.Header.Get("X-Firebase-AppCheck")
    
    appCheckClient, _ := app.AppCheck(ctx)
    _, err := appCheckClient.VerifyToken(token)
    if err != nil {
        http.Error(w, "Unauthorized", http.StatusUnauthorized)
        return
    }
    
    // 处理请求...
}
```

### 不需要使用的场景

- ❌ **只使用 FCM 推送**
- ❌ **服务器到服务器的通信**
- ❌ **不对外暴露 API 端点**

## 八、网络请求详情

### 初始化时的网络请求

```
app.AppCheck(ctx)
    ↓
NewClient() 被调用
    ↓
keyfunc.Get(JWKSUrl, ...)
    ↓
HTTP GET 请求
    URL: https://firebaseappcheck.googleapis.com/v1beta/jwks
    ↓
返回 JWKS (JSON Web Key Set)
    {
      "keys": [
        {
          "kty": "RSA",
          "kid": "...",
          "use": "sig",
          "n": "...",
          "e": "AQAB"
        },
        ...
      ]
    }
    ↓
存储 JWKS，用于验证 Token
    ↓
每 6 小时自动刷新
```

### 验证 Token 时的行为

```
appcheckClient.VerifyToken(token)
    ↓
解析 JWT Token
    ↓
从缓存的 JWKS 中查找对应的公钥
    ↓
验证签名（本地验证，不需要网络请求）
    ↓
验证 claims（iss、aud、exp 等）
    ↓
返回验证结果
```

**注意**：验证 Token 本身**不需要网络请求**，但初始化时需要下载 JWKS。

## 九、代码示例对比

### 示例 1: 只使用 FCM 推送（不需要 AppCheck）

```go
func NewFCMClient(credentialsPath string) (*Client, error) {
    ctx := context.Background()
    
    opts := []option.ClientOption{
        option.WithCredentialsFile(credentialsPath),
    }
    
    app, err := firebase.NewApp(ctx, nil, opts...)
    if err != nil {
        return nil, err
    }
    
    // ✅ 只需要 Messaging Client
    messagingClient, err := app.Messaging(ctx)
    if err != nil {
        return nil, err
    }
    
    // ❌ 不需要 AppCheck
    // appCheckClient, _ := app.AppCheck(ctx)  // 不需要
    
    return &Client{
        messaging: messagingClient,
    }, nil
}
```

### 示例 2: 需要验证 App Check Token 的 API 服务器

```go
type APIHandler struct {
    appCheckClient *appcheck.Client
}

func NewAPIHandler() (*APIHandler, error) {
    ctx := context.Background()
    
    app, err := firebase.NewApp(ctx, nil, option.WithCredentialsFile("..."))
    if err != nil {
        return nil, err
    }
    
    // ✅ 需要 AppCheck Client 来验证 Token
    appCheckClient, err := app.AppCheck(ctx)
    if err != nil {
        return nil, err
    }
    
    return &APIHandler{
        appCheckClient: appCheckClient,
    }, nil
}

func (h *APIHandler) HandleRequest(w http.ResponseWriter, r *http.Request) {
    // 从请求头获取 App Check Token
    token := r.Header.Get("X-Firebase-AppCheck")
    if token == "" {
        http.Error(w, "Missing App Check token", http.StatusUnauthorized)
        return
    }
    
    // ✅ 验证 Token
    _, err := h.appCheckClient.VerifyToken(token)
    if err != nil {
        http.Error(w, "Invalid App Check token", http.StatusUnauthorized)
        return
    }
    
    // Token 验证通过，处理请求
    // ...
}
```

## 十、总结

### AppCheck 的核心要点

| 问题                 | 答案                          |
|----------------------|-------------------------------|
| **会访问服务器吗？** | ✅ 是的，初始化时会下载 JWKS   |
| **检查什么？**       | 验证 App Check Token 是否合法 |
| **用于什么场景？**   | 保护后端 API，防止滥用        |
| **FCM 推送需要吗？** | ❌ 不需要                      |

### 对于 FCM 推送

- ✅ **不需要调用 `app.AppCheck(ctx)`**
- ✅ **不会影响 FCM 推送功能**
- ✅ **移除该调用可以避免不必要的网络请求**
- ✅ **代码更简洁，性能更好**

### 关键理解

1. **AppCheck 是双向验证**：
   - 客户端生成 Token → 后端验证 Token
   - 用于保护后端 API

2. **FCM 推送是单向通信**：
   - 后端 → Firebase → 客户端
   - 不需要 App Check

3. **初始化会访问服务器**：
   - 下载 JWKS（公钥集合）
   - 如果不需要，就是浪费资源

**结论**：对于只使用 FCM 推送的场景，移除 `app.AppCheck(ctx)` 调用是正确的优化。


