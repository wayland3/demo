# Google 原生推送服务说明

## 一、当前推荐：FCM (Firebase Cloud Messaging)

**FCM 是 Google 目前唯一推荐的官方推送服务**，也是 Google 生态系统中的标准推送解决方案。

### FCM 的特点
- ✅ 支持 Android 和 iOS
- ✅ 免费使用（有配额限制）
- ✅ 集成简单，SDK 完善
- ✅ 支持多种推送方式（单设备、多设备、主题、条件推送等）
- ✅ 提供统计和分析功能
- ✅ 与 Firebase 生态系统深度集成

## 二、已废弃：GCM (Google Cloud Messaging)

**GCM 已经被 FCM 完全取代并废弃**

### GCM 的历史
- **2012年**：Google 推出 GCM，用于替代 C2DM (Cloud to Device Messaging)
- **2014年**：GCM 成为 Google 的主要推送服务
- **2016年**：Google 推出 FCM，GCM 被标记为废弃
- **2019年**：GCM 正式停止服务，所有功能迁移到 FCM

### 为什么要废弃 GCM？
1. FCM 功能更强大，支持更多特性
2. FCM 与 Firebase 生态系统集成更好
3. FCM 的 API 更加现代化和易用
4. 统一推送服务的品牌和架构

## 三、Google 原生推送总结

### 答案：**只有 FCM**

Google 原生推送服务只有一种：**Firebase Cloud Messaging (FCM)**

GCM 已经不存在了，FCM 是 Google 目前唯一提供的官方推送服务。

### FCM 的不同使用方式

虽然只有 FCM，但你可以通过不同方式使用它：

#### 1. **HTTP v1 API**（推荐）
```go
// 使用 firebase.google.com/go/v4 SDK
// 这是最现代、最推荐的方式
```

#### 2. **Legacy HTTP API**
```bash
# 使用 HTTP POST 请求
# 兼容性更好，但功能较旧
POST https://fcm.googleapis.com/fcm/send
```

#### 3. **XMPP Server Connection**（已废弃）
- 2018年被废弃
- 不再推荐使用

## 四、FCM 的替代方案

如果你想使用其他推送服务（非 Google 原生），可以考虑：

### 中国市场
- **华为推送 (HMS Push)** - 华为设备
- **小米推送 (Mi Push)** - 小米设备
- **OPPO Push** - OPPO 设备
- **vivo Push** - vivo 设备
- **魅族推送 (Flyme Push)** - 魅族设备

### 第三方服务
- **极光推送 (JPush)** - 国内主流推送服务商
- **个推 (Getui)** - 国内推送服务
- **友盟推送** - 阿里云推送服务
- **OneSignal** - 国际化推送服务

### 跨平台方案
- **UnifiedPush** - 开源推送协议
- **自建推送服务** - 使用 WebSocket 或 MQTT

## 五、推荐策略

### 对于中国市场
由于 FCM 在中国大陆无法使用，建议采用**多通道推送策略**：

```
1. 华为设备 → HMS Push
2. 小米设备 → Mi Push  
3. OPPO设备 → OPPO Push
4. vivo设备 → vivo Push
5. 其他设备 → 极光推送/个推
```

### 对于海外市场
直接使用 **FCM** 即可，这是最简单可靠的方案。

## 六、结论

**Google 原生的推送服务只有 FCM（Firebase Cloud Messaging）**

- ✅ FCM 是目前唯一推荐的 Google 推送服务
- ❌ GCM 已经废弃并停止服务
- 📝 没有其他 Google 原生的推送方式

如果你需要在中国市场提供服务，必须考虑使用国产厂商的推送服务或第三方推送服务商。


