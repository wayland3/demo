package main

import (
	"bytes"
	"context"
	"fmt"
	"io/ioutil"
	"log"
	"math/rand"
	"net/http"
	"strings"
	"time"

	jsoniter "github.com/json-iterator/go"
	"github.com/pkg/errors"
	"github.com/tencentyun/tls-sig-api-v2-golang/tencentyun"
)

// Algorithm 签名算法
type Algorithm string

// 签名算法
const (
	HMACSHA256  Algorithm = "HMAC-SHA256"
	ECDSASHA256 Algorithm = "ECDSA-SHA256"
)

// Signature 签名对象
type Signature struct {
	SDKAppID   int
	PrivateKey string
	Algorithm  Algorithm
}

// GenerateSign 生成签名
func (s Signature) GenerateSign(identifier string, expireTime time.Duration) (sign string, err error) {
	sign, err = tencentyun.GenUserSig(s.SDKAppID, s.PrivateKey, identifier, int(expireTime/time.Second))
	return sign, errors.WithStack(err)
}

type IM struct {
	SDKAppID       int
	Identifier     string
	IdentifierSign string
	URL            string
}

func (im IM) Add(ids ...string) error {
	b, err := im.request(context.Background(), "im_open_login_svc/multiaccount_import", map[string]interface{}{
		"Accounts": ids,
	})
	log.Println(string(b))
	return err
}

type Item struct {
	UserID string
}

func (im IM) Remove(ids ...string) error {
	if len(ids) == 0 {
		return nil
	}

	items := make([]Item, 0, 100)
	for i, id := range ids {
		items = append(items, Item{id})
		if (i+1)%100 == 0 || len(ids) == i+1 {
			b, err := im.request(context.Background(), "/im_open_login_svc/account_delete", map[string]interface{}{"DeleteItem": items})
			log.Println(string(b))
			if err != nil {
				return err
			}

			items = make([]Item, 100)
		}
	}

	return nil
}

func (im IM) request(ctx context.Context, path string, body interface{}) ([]byte, error) {
	data, err := jsoniter.Marshal(body)
	if err != nil {
		return nil, fmt.Errorf("json encode request body, %w", err)
	}

	req, err := http.NewRequestWithContext(ctx, http.MethodPost, im.URL+strings.TrimLeft(path, "/"), bytes.NewReader(data))
	if err != nil {
		return nil, errors.WithStack(err)
	}

	rand.Seed(time.Now().UnixNano())
	values := req.URL.Query()
	values["sdkappid"] = []string{fmt.Sprintf("%d", im.SDKAppID)}
	values["identifier"] = []string{im.Identifier}
	values["usersig"] = []string{im.IdentifierSign}
	values["random"] = []string{fmt.Sprintf("%d", rand.Int())}
	values["contenttype"] = []string{"json"}
	req.URL.RawQuery = values.Encode()
	log.Println(req.URL)

	response, err := new(http.Client).Do(req)
	if err != nil {
		return nil, errors.WithStack(err)
	}

	defer response.Body.Close()

	res, err := ioutil.ReadAll(response.Body)
	if err != nil {
		return nil, errors.WithStack(err)
	}

	return res, nil
}
