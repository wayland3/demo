# 文件下载问题排查指南

## 一、常见问题

### 1. 浏览器不触发下载，而是直接打开文件

**原因**：某些浏览器（如 Chrome、Firefox）对于常见的文件类型（如 `.txt`、`.pdf`、`.jpg` 等），默认会在浏览器中打开，而不是下载。

**解决方法**：

#### 方法1：使用右键菜单
- 在文件链接上**右键** → 选择"另存为"或"链接另存为"

#### 方法2：使用 `curl` 或 `wget` 命令行工具
```bash
# 使用 curl 下载
curl -O http://localhost:8000/filename.txt

# 使用 wget 下载
wget http://localhost:8000/filename.txt
```

#### 方法3：修改响应头（强制下载所有文件）
将 `Content-Disposition` 改为：
```
Content-Disposition: attachment; filename="..."
```

### 2. 文件名包含中文或特殊字符时乱码

**原因**：HTTP 响应头中的文件名需要正确编码。

**解决方法**：
代码已经使用 `RFC 5987` 格式支持 UTF-8 文件名：
```python
filename*=UTF-8''{url_encoded_filename}
```

### 3. 404 错误：文件未找到

**可能原因**：
- 文件路径不正确
- 文件不存在
- 路径中包含特殊字符

**排查步骤**：
1. 检查文件是否存在于服务目录中
2. 检查 URL 路径是否正确
3. 查看服务器日志输出

### 4. 403 错误：访问被拒绝

**可能原因**：
- 文件不在服务目录内（路径安全检查）
- 文件权限不足

**排查步骤**：
1. 确认文件在服务目录内
2. 检查文件读取权限：`ls -l filename`

### 5. 连接被重置或下载中断

**可能原因**：
- 网络不稳定
- 文件太大，传输超时
- 客户端提前关闭连接

**解决方法**：
- 这是正常现象，服务器已经正确处理了这些错误
- 可以重试下载

## 二、测试下载功能

### 创建测试文件

```bash
# 创建一个测试文件
echo "这是一个测试文件" > test.txt

# 创建一个中文文件名的测试文件
echo "测试内容" > "测试文件.txt"
```

### 测试命令

```bash
# 1. 启动服务
python3 file_server.py -d . -p 8000

# 2. 在浏览器中访问
# http://localhost:8000

# 3. 使用 curl 测试下载
curl -O http://localhost:8000/test.txt

# 4. 使用 wget 测试下载
wget http://localhost:8000/test.txt

# 5. 使用 Python requests 测试
python3 -c "import requests; r = requests.get('http://localhost:8000/test.txt'); open('downloaded.txt', 'wb').write(r.content)"
```

## 三、使用调试版本

如果遇到问题，可以使用调试版本查看详细信息：

```bash
python3 file_server_debug.py -d . -p 8000
```

调试版本会输出：
- 请求路径
- 文件路径解析过程
- 响应头信息
- 传输进度
- 错误信息

## 四、推荐的下载方式

### 对于不同文件类型：

1. **文本文件** (`.txt`, `.md`, `.log`)
   - 浏览器通常直接打开
   - 使用右键 → "另存为" 下载

2. **图片文件** (`.jpg`, `.png`, `.gif`)
   - 浏览器通常直接显示
   - 使用右键 → "图片另存为" 下载

3. **文档文件** (`.pdf`, `.doc`, `.docx`)
   - 浏览器可能直接打开或下载
   - 可以直接点击链接下载

4. **压缩文件** (`.zip`, `.tar`, `.gz`)
   - 浏览器通常直接下载
   - 直接点击链接即可

5. **可执行文件** (`.exe`, `.dmg`, `.pkg`)
   - 浏览器通常直接下载
   - 直接点击链接即可

## 五、强制下载所有文件类型

如果需要所有文件类型都强制下载，可以修改响应头：

```python
# 在 send_file 方法中，将 Content-Type 改为：
self.send_header('Content-Type', 'application/octet-stream')
```

这样浏览器会强制下载所有文件，而不是尝试打开。

## 六、验证下载是否成功

下载文件后，可以验证：

```bash
# 检查文件大小
ls -lh downloaded_file

# 检查文件内容（文本文件）
cat downloaded_file

# 比较原始文件和下载文件
diff original_file downloaded_file
```

## 七、常见错误信息

| 错误信息                    | 原因                 | 解决方法                     |
|-----------------------------|----------------------|------------------------------|
| `404 File Not Found`        | 文件不存在           | 检查文件路径和文件名         |
| `403 Access Denied`         | 路径不安全或权限不足 | 检查文件是否在服务目录内     |
| `500 Internal Server Error` | 服务器内部错误       | 查看服务器日志，检查文件权限 |
| `Connection reset`          | 连接被重置           | 这是正常的，可以重试         |

## 八、最佳实践

1. **使用命令行工具测试**
   - `curl` 或 `wget` 可以更可靠地测试下载功能

2. **检查文件权限**
   ```bash
   chmod 644 filename  # 确保文件可读
   ```

3. **测试不同文件类型**
   - 测试文本、图片、压缩包等不同类型文件

4. **使用调试版本排查问题**
   - 遇到问题时使用 `file_server_debug.py` 查看详细信息

5. **检查网络连接**
   - 确保客户端和服务器网络连接正常


