package fcm

import (
	"database/sql"
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"time"

	_ "github.com/go-sql-driver/mysql"
)

// DeviceTokenRequest 客户端发送的 Token 注册请求
type DeviceTokenRequest struct {
	Token    string `json:"token"`    // FCM Token
	UserID   string `json:"userId"`   // 用户ID
	Platform string `json:"platform"` // "android" 或 "ios"
	DeviceID string `json:"deviceId"` // 设备ID（可选）
}

// DeviceTokenResponse 响应结构
type DeviceTokenResponse struct {
	Status  string `json:"status"`
	Message string `json:"message"`
}

// TokenHandler Token 处理器
type TokenHandler struct {
	db *sql.DB
}

// NewTokenHandler 创建 Token 处理器
func NewTokenHandler(db *sql.DB) *TokenHandler {
	return &TokenHandler{db: db}
}

// RegisterTokenHandler HTTP 处理器：注册设备 Token
func (h *TokenHandler) RegisterTokenHandler(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		return
	}

	// 解析请求
	var req DeviceTokenRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		http.Error(w, fmt.Sprintf("Invalid request: %v", err), http.StatusBadRequest)
		return
	}

	// 验证必填字段
	if req.Token == "" {
		http.Error(w, "Token is required", http.StatusBadRequest)
		return
	}

	if req.UserID == "" {
		http.Error(w, "UserID is required", http.StatusBadRequest)
		return
	}

	if req.Platform != "android" && req.Platform != "ios" {
		http.Error(w, "Platform must be 'android' or 'ios'", http.StatusBadRequest)
		return
	}

	// 保存或更新 Token
	if err := h.saveOrUpdateToken(&req); err != nil {
		log.Printf("保存 Token 失败: %v", err)
		http.Error(w, "Failed to save token", http.StatusInternalServerError)
		return
	}

	log.Printf("Token 注册成功: UserID=%s, Platform=%s, Token=%s...",
		req.UserID, req.Platform, req.Token[:20])

	// 返回成功响应
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(DeviceTokenResponse{
		Status:  "success",
		Message: "Token registered successfully",
	})
}

// saveOrUpdateToken 保存或更新 Token 到数据库
func (h *TokenHandler) saveOrUpdateToken(req *DeviceTokenRequest) error {
	now := time.Now()

	// 检查 Token 是否已存在
	var existingID int64
	err := h.db.QueryRow(
		"SELECT id FROM device_tokens WHERE token = ?",
		req.Token,
	).Scan(&existingID)

	if err == sql.ErrNoRows {
		// Token 不存在，插入新记录
		_, err = h.db.Exec(`
			INSERT INTO device_tokens (user_id, token, platform, device_id, created_at, updated_at)
			VALUES (?, ?, ?, ?, ?, ?)
		`, req.UserID, req.Token, req.Platform, req.DeviceID, now, now)
		return err
	} else if err != nil {
		return fmt.Errorf("查询 Token 失败: %w", err)
	}

	// Token 已存在，更新记录
	_, err = h.db.Exec(`
		UPDATE device_tokens 
		SET user_id = ?, platform = ?, device_id = ?, updated_at = ?
		WHERE token = ?
	`, req.UserID, req.Platform, req.DeviceID, now, req.Token)
	return err
}

// GetUserTokens 获取用户的所有 Token
func (h *TokenHandler) GetUserTokens(userID string) ([]string, error) {
	rows, err := h.db.Query(
		"SELECT token FROM device_tokens WHERE user_id = ?",
		userID,
	)
	if err != nil {
		return nil, fmt.Errorf("查询用户 Token 失败: %w", err)
	}
	defer rows.Close()

	var tokens []string
	for rows.Next() {
		var token string
		if err := rows.Scan(&token); err != nil {
			return nil, fmt.Errorf("扫描 Token 失败: %w", err)
		}
		tokens = append(tokens, token)
	}

	return tokens, rows.Err()
}

// DeleteToken 删除 Token（当 Token 失效时）
func (h *TokenHandler) DeleteToken(token string) error {
	_, err := h.db.Exec("DELETE FROM device_tokens WHERE token = ?", token)
	return err
}

// CreateTokenTable 创建 Token 表的 SQL（示例）
// 在实际项目中，应该使用数据库迁移工具
const CreateTokenTableSQL = `
CREATE TABLE IF NOT EXISTS device_tokens (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id VARCHAR(255) NOT NULL,
    token VARCHAR(512) NOT NULL UNIQUE,
    platform VARCHAR(20) NOT NULL,
    device_id VARCHAR(255),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_user_id (user_id),
    INDEX idx_token (token)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
`

// 使用示例：
/*
func main() {
    // 连接数据库
    db, err := sql.Open("mysql", "user:password@tcp(localhost:3306)/dbname")
    if err != nil {
        log.Fatal(err)
    }
    defer db.Close()

    // 创建表（仅第一次运行时）
    db.Exec(CreateTokenTableSQL)

    // 创建 Token 处理器
    handler := NewTokenHandler(db)

    // 注册 HTTP 路由
    http.HandleFunc("/api/device/register", handler.RegisterTokenHandler)

    // 启动服务器
    log.Println("服务器启动在 :8080")
    log.Fatal(http.ListenAndServe(":8080", nil))
}
*/

