# 如何获取 FCM 设备 Token

FCM 设备 Token 是 Firebase 为每个设备生成的一个**唯一标识符**，用于向特定设备发送推送通知。Token 是在**客户端应用**中获取的，然后需要发送到后端服务器保存。

## 一、Token 获取流程

```
客户端应用启动
    ↓
初始化 Firebase SDK
    ↓
获取 FCM Token
    ↓
将 Token 发送到后端服务器保存
    ↓
后端服务器使用 Token 发送推送
```

## 二、Android 客户端获取 Token

### 步骤 1：添加 Firebase 依赖

在项目的 `build.gradle` (Module: app) 文件中添加：

```gradle
dependencies {
    // Firebase Cloud Messaging
    implementation 'com.google.firebase:firebase-messaging:23.2.1'
    // Firebase BoM（推荐，用于版本管理）
    implementation platform('com.google.firebase:firebase-bom:32.5.0')
    implementation 'com.google.firebase:firebase-messaging'
}
```

在项目根目录的 `build.gradle` 中添加：

```gradle
buildscript {
    dependencies {
        classpath 'com.google.gms:google-services:4.4.0'
    }
}
```

在 `app/build.gradle` 文件末尾添加：

```gradle
apply plugin: 'com.google.gms.google-services'
```

### 步骤 2：下载并配置 `google-services.json`

1. 在 [Firebase Console](https://console.firebase.google.com/) 中创建项目
2. 添加 Android 应用，填写包名（例如：`com.example.myapp`）
3. 下载 `google-services.json` 文件
4. 将文件放到 `app/` 目录下

### 步骤 3：在应用中获取 Token

创建 `FirebaseMessagingService` 继承类：

```java
package com.example.myapp;

import android.util.Log;
import com.google.firebase.messaging.FirebaseMessagingService;
import com.google.firebase.messaging.RemoteMessage;

public class MyFirebaseMessagingService extends FirebaseMessagingService {
    
    private static final String TAG = "FCMService";
    
    @Override
    public void onNewToken(String token) {
        Log.d(TAG, "新的 FCM Token: " + token);
        
        // 将 Token 发送到后端服务器
        sendTokenToServer(token);
    }
    
    @Override
    public void onMessageReceived(RemoteMessage remoteMessage) {
        // 处理接收到的推送消息
        Log.d(TAG, "收到推送消息: " + remoteMessage.getNotification().getBody());
    }
    
    private void sendTokenToServer(String token) {
        // 通过 HTTP API 将 Token 发送到后端
        // 示例：使用 Retrofit/OkHttp 发送 POST 请求
        // POST /api/device/token
        // Body: { "token": token, "deviceId": deviceId }
    }
    
    // 获取当前 Token（如果已存在）
    public static void getCurrentToken() {
        FirebaseMessaging.getInstance().getToken()
            .addOnCompleteListener(task -> {
                if (!task.isSuccessful()) {
                    Log.w(TAG, "获取 Token 失败", task.getException());
                    return;
                }
                
                // 获取 Token 成功
                String token = task.getResult();
                Log.d(TAG, "当前 FCM Token: " + token);
                
                // 发送到服务器
                sendTokenToServer(token);
            });
    }
}
```

在 `AndroidManifest.xml` 中注册服务：

```xml
<service
    android:name=".MyFirebaseMessagingService"
    android:exported="false">
    <intent-filter>
        <action android:name="com.google.firebase.MESSAGING_EVENT" />
    </intent-filter>
</service>
```

### 步骤 4：在应用启动时获取 Token

在 `MainActivity` 或应用初始化代码中：

```java
import com.google.firebase.messaging.FirebaseMessaging;

public class MainActivity extends AppCompatActivity {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        
        // 获取 FCM Token
        FirebaseMessaging.getInstance().getToken()
            .addOnCompleteListener(task -> {
                if (!task.isSuccessful()) {
                    Log.w("MainActivity", "获取 Token 失败", task.getException());
                    return;
                }
                
                String token = task.getResult();
                Log.d("MainActivity", "FCM Token: " + token);
                
                // 将 Token 发送到后端服务器
                sendTokenToBackend(token);
            });
    }
    
    private void sendTokenToBackend(String token) {
        // 使用 HTTP 客户端发送 Token 到后端
        // 示例：
        // POST https://your-api.com/api/device/register
        // {
        //   "token": token,
        //   "userId": userId,
        //   "platform": "android"
        // }
    }
}
```

## 三、iOS 客户端获取 Token

### 步骤 1：配置 Xcode 项目

1. 在 [Firebase Console](https://console.firebase.google.com/) 中添加 iOS 应用
2. 下载 `GoogleService-Info.plist` 文件
3. 将文件拖入 Xcode 项目

### 步骤 2：安装 Firebase SDK

使用 CocoaPods，在 `Podfile` 中添加：

```ruby
pod 'Firebase/Messaging'
```

然后运行：

```bash
pod install
```

### 步骤 3：在应用中获取 Token

在 `AppDelegate.swift` 或 `AppDelegate.m` 中：

**Swift 版本：**

```swift
import UIKit
import FirebaseCore
import FirebaseMessaging

@main
class AppDelegate: UIResponder, UIApplicationDelegate, UNUserNotificationCenterDelegate, MessagingDelegate {
    
    func application(_ application: UIApplication, didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey: Any]?) -> Bool {
        
        // 初始化 Firebase
        FirebaseApp.configure()
        
        // 设置推送通知代理
        UNUserNotificationCenter.current().delegate = self
        Messaging.messaging().delegate = self
        
        // 请求推送权限
        UNUserNotificationCenter.current().requestAuthorization(options: [.alert, .badge, .sound]) { granted, error in
            if granted {
                DispatchQueue.main.async {
                    application.registerForRemoteNotifications()
                }
            }
        }
        
        return true
    }
    
    // 获取 APNs Token 后，Firebase 会自动获取 FCM Token
    func application(_ application: UIApplication, didRegisterForRemoteNotificationsWithDeviceToken deviceToken: Data) {
        Messaging.messaging().apnsToken = deviceToken
    }
    
    // 获取 FCM Token
    func messaging(_ messaging: Messaging, didReceiveRegistrationToken fcmToken: String?) {
        print("FCM Token: \(fcmToken ?? "nil")")
        
        if let token = fcmToken {
            // 将 Token 发送到后端服务器
            sendTokenToBackend(token: token)
        }
    }
    
    private func sendTokenToBackend(token: String) {
        // 使用 URLSession 发送 Token 到后端
        // POST https://your-api.com/api/device/register
        // {
        //   "token": token,
        //   "userId": userId,
        //   "platform": "ios"
        // }
    }
    
    // Token 更新时会被调用
    func messaging(_ messaging: Messaging, didReceiveRegistrationToken fcmToken: String?) {
        print("新的 FCM Token: \(fcmToken ?? "nil")")
        
        if let token = fcmToken {
            sendTokenToBackend(token: token)
        }
    }
}
```

**Objective-C 版本：**

```objc
#import "AppDelegate.h"
#import <FirebaseCore/FirebaseCore.h>
#import <FirebaseMessaging/FirebaseMessaging.h>
#import <UserNotifications/UserNotifications.h>

@interface AppDelegate () <UNUserNotificationCenterDelegate, FIRMessagingDelegate>
@end

@implementation AppDelegate

- (BOOL)application:(UIApplication *)application didFinishLaunchingWithOptions:(NSDictionary *)launchOptions {
    
    // 初始化 Firebase
    [FIRApp configure];
    
    // 设置代理
    [UNUserNotificationCenter currentNotificationCenter].delegate = self;
    [FIRMessaging messaging].delegate = self;
    
    // 请求推送权限
    [[UNUserNotificationCenter currentNotificationCenter] requestAuthorizationWithOptions:(UNAuthorizationOptionAlert | UNAuthorizationOptionBadge | UNAuthorizationOptionSound) completionHandler:^(BOOL granted, NSError * _Nullable error) {
        if (granted) {
            dispatch_async(dispatch_get_main_queue(), ^{
                [application registerForRemoteNotifications];
            });
        }
    }];
    
    return YES;
}

// 获取 APNs Token
- (void)application:(UIApplication *)application didRegisterForRemoteNotificationsWithDeviceToken:(NSData *)deviceToken {
    [FIRMessaging messaging].APNSToken = deviceToken;
}

// 获取 FCM Token
- (void)messaging:(FIRMessaging *)messaging didReceiveRegistrationToken:(NSString *)fcmToken {
    NSLog(@"FCM Token: %@", fcmToken);
    
    // 发送到后端
    [self sendTokenToBackend:fcmToken];
}

- (void)sendTokenToBackend:(NSString *)token {
    // 发送 HTTP 请求到后端服务器
}

@end
```

## 四、后端服务器接收和存储 Token

后端需要提供一个 API 接口来接收客户端发送的 Token：

### Go 后端示例

```go
package main

import (
    "encoding/json"
    "log"
    "net/http"
)

type DeviceTokenRequest struct {
    Token    string `json:"token"`
    UserID   string `json:"userId"`
    Platform string `json:"platform"` // "android" 或 "ios"
    DeviceID string `json:"deviceId"`
}

// 存储 Token 的数据库表结构
// CREATE TABLE device_tokens (
//     id BIGINT PRIMARY KEY AUTO_INCREMENT,
//     user_id VARCHAR(255),
//     token VARCHAR(512) UNIQUE,
//     platform VARCHAR(20),
//     device_id VARCHAR(255),
//     created_at TIMESTAMP,
//     updated_at TIMESTAMP
// )

func registerDeviceToken(w http.ResponseWriter, r *http.Request) {
    if r.Method != http.MethodPost {
        http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
        return
    }
    
    var req DeviceTokenRequest
    if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
        http.Error(w, "Invalid request", http.StatusBadRequest)
        return
    }
    
    // 验证 Token 格式
    if req.Token == "" {
        http.Error(w, "Token is required", http.StatusBadRequest)
        return
    }
    
    // 保存到数据库
    // 1. 检查 Token 是否已存在
    // 2. 如果存在，更新 user_id 和 updated_at
    // 3. 如果不存在，插入新记录
    
    log.Printf("收到设备 Token: %s (用户: %s, 平台: %s)", 
        req.Token, req.UserID, req.Platform)
    
    // 保存到数据库的代码...
    // db.SaveOrUpdateToken(req)
    
    w.WriteHeader(http.StatusOK)
    json.NewEncoder(w).Encode(map[string]string{
        "status": "success",
        "message": "Token registered",
    })
}
```

## 五、Token 的重要特性

### 1. Token 会变化
- 应用重新安装时
- 应用清除数据时
- Firebase 项目重新生成密钥时
- Token 过期时（虽然很少发生）

### 2. Token 更新
当 Token 更新时，`onNewToken()` (Android) 或 `messaging:didReceiveRegistrationToken:` (iOS) 会被调用，需要再次发送到后端。

### 3. Token 格式
```
示例 Token 格式：
cX8Yz9aBcDeFgHiJkLmNoPqRsTuVwXyZaBcDeFgHiJkLmNoPqRsTuVwXyZaBcDeFgHiJkLmNoPqRsTuVwXyZaBcDeFgHiJkLmNoPqRsTuVwXyZaBcDeFgHiJkLmNoPqRsTuVwXyZaBcDeFgHiJkLmNoPqRsTuVwXyZaBc
```

Token 是一个很长的字符串，通常有 100+ 个字符。

## 六、完整流程示例

```
1. 用户安装应用
   ↓
2. 应用启动，初始化 Firebase SDK
   ↓
3. 请求推送权限（iOS 需要，Android 不需要）
   ↓
4. 获取 FCM Token
   ↓
5. 将 Token + UserID 发送到后端 API
   POST /api/device/register
   {
     "token": "cX8Yz9aBc...",
     "userId": "user123",
     "platform": "android"
   }
   ↓
6. 后端保存 Token 到数据库
   ↓
7. 需要发送推送时，后端从数据库读取 Token
   ↓
8. 使用 FCM SDK 发送推送
```

## 七、测试 Token

在开发阶段，你可以：

1. 在客户端打印 Token 到日志
2. 在客户端显示 Token（调试模式）
3. 通过 API 查询用户的 Token
4. 使用 Firebase Console 的"测试消息"功能直接发送推送

## 注意事项

1. **Token 是敏感信息**：不应该在日志中永久记录，或暴露在客户端可见的地方
2. **Token 需要绑定用户**：保存 Token 时应该关联用户 ID，以便向特定用户推送
3. **处理 Token 失效**：当推送失败时，可能需要更新或删除无效的 Token
4. **多设备支持**：一个用户可能有多个设备（手机、平板），每个设备有独立的 Token


