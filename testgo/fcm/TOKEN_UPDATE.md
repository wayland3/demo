# FCM Token 更新机制

## 一、Token 的生命周期

### Token 的特点

1. **Token 是长期有效的**：正常情况下，FCM Token **不会自动过期**
2. **Token 可能会变化**：在某些特定情况下，Token 会被重新生成
3. **需要监听 Token 更新**：应用需要实时监听 Token 的变化并同步到服务器

## 二、Token 何时会更新？

### 自动更新的场景

#### 1. **应用重新安装**
```
用户卸载应用 → 重新安装 → Token 会改变
```
- **原因**：Firebase 会为新的安装生成新的 Token
- **频率**：仅在重装时发生

#### 2. **应用清除数据**
```
Android: 设置 → 应用 → 清除数据 → Token 会改变
iOS: 删除应用重新安装 → Token 会改变
```
- **原因**：清除数据会删除 Firebase 的本地存储
- **频率**：用户操作触发，不常见

#### 3. **恢复出厂设置**
```
设备恢复出厂设置 → 重新安装应用 → Token 会改变
```

#### 4. **应用数据被系统清理**
```
系统清理缓存 → 在某些极端情况下可能清除 Token
```

#### 5. **Firebase 项目配置变更**
```
- Firebase 项目被删除后重新创建
- 应用在 Firebase Console 中被删除后重新添加
- 包名（Android）/ Bundle ID（iOS）改变
```

### Token 不会更新的情况

✅ **正常情况下不需要更新**：
- 应用正常使用
- 应用更新（升级版本）
- 设备重启
- 应用进程被系统杀死后重启
- 网络断开重连

## 三、Token 更新机制

### Android 获取 Token 更新

Firebase SDK 提供了自动监听 Token 更新的机制：

```java
public class MyFirebaseMessagingService extends FirebaseMessagingService {
    
    @Override
    public void onNewToken(String token) {
        // ⚠️ 这个方法会在以下情况被调用：
        // 1. 应用首次安装时
        // 2. Token 被刷新时（重新安装、清除数据等）
        // 3. 应用恢复时（某些情况下）
        
        Log.d(TAG, "新的 Token: " + token);
        
        // ✅ 必须将新 Token 发送到服务器
        sendTokenToServer(token);
    }
}
```

**重要**：`onNewToken()` 是获取 Token 更新的**唯一可靠方式**。

### iOS 获取 Token 更新

iOS 通过代理方法监听 Token 更新：

**Swift:**
```swift
func messaging(_ messaging: Messaging, didReceiveRegistrationToken fcmToken: String?) {
    // ⚠️ 这个方法会在以下情况被调用：
    // 1. 应用首次启动时
    // 2. Token 被刷新时
    
    guard let token = fcmToken else { return }
    print("新的 Token: \(token)")
    
    // ✅ 必须将新 Token 发送到服务器
    sendTokenToServer(token: token)
}
```

**Objective-C:**
```objc
- (void)messaging:(FIRMessaging *)messaging didReceiveRegistrationToken:(NSString *)fcmToken {
    NSLog(@"新的 Token: %@", fcmToken);
    [self sendTokenToServer:fcmToken];
}
```

## 四、最佳实践

### 1. 客户端：始终监听 Token 更新

#### Android 完整示例

```java
public class MyFirebaseMessagingService extends FirebaseMessagingService {
    
    private static final String TAG = "FCMService";
    private static final String PREFS_NAME = "fcm_prefs";
    private static final String KEY_TOKEN = "last_token";
    
    @Override
    public void onNewToken(String token) {
        super.onNewToken(token);
        
        Log.d(TAG, "Token 更新: " + token);
        
        // 保存到 SharedPreferences
        SharedPreferences prefs = getSharedPreferences(PREFS_NAME, MODE_PRIVATE);
        String lastToken = prefs.getString(KEY_TOKEN, null);
        
        // 如果 Token 改变，发送到服务器
        if (!token.equals(lastToken)) {
            prefs.edit().putString(KEY_TOKEN, token).apply();
            sendTokenToServer(token);
        }
    }
    
    private void sendTokenToServer(String token) {
        // 发送到后端 API
        // 应该包含用户ID、平台等信息
    }
}
```

#### iOS 完整示例

```swift
func messaging(_ messaging: Messaging, didReceiveRegistrationToken fcmToken: String?) {
    guard let token = fcmToken else { return }
    
    let lastToken = UserDefaults.standard.string(forKey: "lastFCMToken")
    
    // 如果 Token 改变，发送到服务器
    if token != lastToken {
        UserDefaults.standard.set(token, forKey: "lastFCMToken")
        sendTokenToServer(token: token)
    }
}
```

### 2. 客户端：应用启动时检查 Token

即使有了 `onNewToken()` 监听，也应该在应用启动时主动获取一次：

```java
// Android
public class MainActivity extends AppCompatActivity {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        
        // 应用启动时获取当前 Token
        FirebaseMessaging.getInstance().getToken()
            .addOnCompleteListener(task -> {
                if (task.isSuccessful()) {
                    String token = task.getResult();
                    checkAndUpdateToken(token);
                }
            });
    }
    
    private void checkAndUpdateToken(String currentToken) {
        SharedPreferences prefs = getSharedPreferences("fcm_prefs", MODE_PRIVATE);
        String lastToken = prefs.getString("last_token", null);
        
        // 如果 Token 不同，发送到服务器
        if (!currentToken.equals(lastToken)) {
            prefs.edit().putString("last_token", currentToken).apply();
            sendTokenToServer(currentToken);
        }
    }
}
```

### 3. 后端：处理 Token 更新

后端应该支持 Token 的更新，而不是仅支持新增：

```go
// 后端保存 Token 时，应该支持更新
func (h *TokenHandler) saveOrUpdateToken(req *DeviceTokenRequest) error {
    // 检查 Token 是否存在
    var existingUserID string
    err := h.db.QueryRow(
        "SELECT user_id FROM device_tokens WHERE token = ?",
        req.Token,
    ).Scan(&existingUserID)
    
    if err == sql.ErrNoRows {
        // Token 不存在，插入
        _, err = h.db.Exec(`
            INSERT INTO device_tokens (user_id, token, platform, updated_at)
            VALUES (?, ?, ?, ?)
        `, req.UserID, req.Token, req.Platform, time.Now())
    } else if err != nil {
        return err
    } else {
        // Token 存在但用户不同，可能是用户更换了设备
        // 或者同一个设备被不同用户使用
        if existingUserID != req.UserID {
            // 更新用户ID和更新时间
            _, err = h.db.Exec(`
                UPDATE device_tokens 
                SET user_id = ?, updated_at = ?
                WHERE token = ?
            `, req.UserID, time.Now(), req.Token)
        } else {
            // 用户相同，只更新更新时间
            _, err = h.db.Exec(`
                UPDATE device_tokens 
                SET updated_at = ?
                WHERE token = ?
            `, time.Now(), req.Token)
        }
    }
    
    return err
}
```

### 4. 后端：处理无效 Token

当推送失败时，应该删除无效的 Token：

```go
func (c *FCMClient) SendToDevice(token string, msg *Message) error {
    response, err := c.messaging.Send(ctx, message)
    if err != nil {
        // 检查是否是无效 Token 错误
        if messaging.IsInvalidArgument(err) || messaging.IsRegistrationTokenNotRegistered(err) {
            // Token 无效，从数据库删除
            log.Printf("Token 无效，删除: %s", token)
            tokenHandler.DeleteToken(token)
        }
        return err
    }
    return nil
}
```

## 五、Token 更新频率总结

### 实际更新频率

| 场景             | 频率       | 说明                        |
|------------------|------------|-----------------------------|
| **正常使用**     | ❌ 不更新   | Token 长期有效，不需要更新  |
| **应用重装**     | 每次重装   | 每次重新安装应用时更新      |
| **清除数据**     | 每次清除   | 用户手动清除应用数据时更新  |
| **恢复出厂**     | 每次恢复   | 设备恢复出厂设置时更新      |
| **项目配置变更** | 配置变更时 | Firebase 项目配置改变时更新 |

### 关键要点

1. **Token 不是定期更新的**：没有"有效期"概念，不需要定期刷新
2. **更新是事件驱动的**：只在特定事件发生时更新
3. **必须监听更新事件**：通过 `onNewToken()` / `didReceiveRegistrationToken` 监听
4. **启动时检查**：应用启动时应该验证 Token 是否已同步到服务器

## 六、推荐的实现策略

### 客户端策略

```
应用启动
    ↓
1. 获取当前 Token
    ↓
2. 检查本地保存的 Token 是否相同
    ↓
3. 如果不同，发送到服务器
    ↓
4. 监听 onNewToken() 回调
    ↓
5. 当收到新 Token 时，立即发送到服务器
```

### 后端策略

```
收到 Token 注册请求
    ↓
1. 检查 Token 是否已存在
    ↓
2. 如果存在：
   - 检查用户ID是否相同
   - 更新更新时间
    ↓
3. 如果不存在：
   - 插入新记录
    ↓
4. 返回成功响应
```

### 推送失败处理策略

```
发送推送
    ↓
推送失败？
    ↓
是 → 检查错误类型
    ↓
Token 无效？
    ↓
是 → 删除数据库中的 Token
    ↓
通知客户端重新获取 Token（可选）
```

## 七、常见问题

### Q1: Token 有有效期吗？
**A:** 没有固定的有效期。Token 在正常情况下不会过期，只有在特定事件（重装应用等）时才会改变。

### Q2: 需要定期刷新 Token 吗？
**A:** 不需要。Token 不会定期过期，不需要主动刷新。只需要监听 `onNewToken()` 回调即可。

### Q3: Token 多久会变化一次？
**A:** 变化频率取决于用户行为：
- 大多数用户：Token 很少变化（可能几个月甚至几年不变）
- 经常重装应用的用户：每次重装都会变化

### Q4: 如何确保 Token 是最新的？
**A:** 
1. 实现 `onNewToken()` 回调，自动接收更新
2. 应用启动时获取当前 Token 并与服务器同步
3. 推送失败时，删除无效 Token，让客户端重新注册

### Q5: 一个用户可以有多个 Token 吗？
**A:** 可以。一个用户可能有多台设备（手机、平板），每台设备都有独立的 Token。后端应该保存用户的所有 Token，推送时可以批量发送。

## 八、总结

- ✅ **Token 不会定期过期**，正常情况下长期有效
- ✅ **Token 只在特定事件时更新**（重装应用、清除数据等）
- ✅ **必须监听 `onNewToken()` 回调**，实时接收 Token 更新
- ✅ **应用启动时检查 Token**，确保与服务器同步
- ✅ **后端支持 Token 更新**，而不是仅支持新增
- ✅ **处理推送失败**，删除无效 Token

**核心原则：Token 更新是事件驱动的，不是时间驱动的。**


