package email

import (
	"crypto/tls"
	"io"

	"github.com/pkg/errors"
	"gopkg.in/gomail.v2"
)

// Email 邮件参数
type Email struct {
	Subject  string
	Body     string
	To       []string
	Filename string
	File     io.Reader
}

// Sender 邮件发送器
type Sender interface {
	Send(Email) error
}

// Client 邮件客户端
type Client struct {
	Host     string
	Port     int
	Username string
	Password string
	From     string
}

// NewClient 构造函数
func NewClient(conf Config) Sender {
	return &Client{
		Host:     conf.Host,
		Port:     conf.Port,
		Username: conf.Username,
		Password: conf.Password,
		From:     conf.From,
	}
}
func (c *Client) buildMessage(e Email) (*gomail.Message, error) {
	if len(e.To) == 0 {
		return nil, errors.New("email empty receiver")
	}

	m := gomail.NewMessage()
	m.SetHeader("From", c.From)
	m.SetHeader("To", e.To...)
	m.SetHeader("Subject", e.Subject)
	m.SetBody("text/plain", e.Body)

	if e.Filename == "" || e.File == nil {
		return m, nil
	}
	m.Attach(e.Filename, gomail.SetCopyFunc(func(w io.Writer) error {
		_, err := io.Copy(w, e.File)
		return errors.WithStack(err)
	}))
	return m, nil
}

// Send 发送邮件
func (c *Client) Send(e Email) error {
	m, err := c.buildMessage(e)
	if err != nil {
		return err
	}

	d := gomail.NewDialer(c.Host, c.Port, c.Username, c.Password)
	d.TLSConfig = &tls.Config{InsecureSkipVerify: true}
	err = d.DialAndSend(m)
	return errors.WithStack(err)
}
