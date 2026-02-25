package fmtx

import (
	"fmt"
	"testing"
)

var (
	msg = "agkinbiohois %w %s %d %f %v"
	err = &E{A: 1}
)

type E struct {
	A int
}

func (e *E) Error() string {
	return fmt.Sprintf("E: %d", e.A)
}

func CommonErrorf() error {
	if err != nil {
		return fmt.Errorf(msg, err, "test", 1, 1.2345, []int{1, 2, 3})
	}
	return nil
}

func EasyErrorf() error {
	return Errorf(msg, err, "test", 1, 1.2345, []int{1, 2, 3})
}

func BenchmarkCommonErrorf(t *testing.B) {
	for i := 0; i < t.N; i++ {
		err := CommonErrorf()
		_ = err
	}
}

func BenchmarkEasyErrorf(t *testing.B) {
	for i := 0; i < t.N; i++ {
		err := EasyErrorf()
		_ = err
	}
}

func TestErrorf(t *testing.T) {
	fmt.Printf("%  d\n", 12)
}
