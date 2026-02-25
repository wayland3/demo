package fmtx

import (
	"fmt"
)

var pattern = "%[#|0|+|-]w"

// Errorf 用于简化返回error的函数
// 用法与fmt.Errorf一致，相对于fmt.Errorf，本函数当error为nil时，
// 不会创建error对象，而是直接返回nil
func Errorf(format string, a ...any) error {
	// 从format解析出所有参数
	// 找到%w的位置，如果没有，则直接调用fmt.Errorf
	// 如果有，则判断%w对应位置的a中参数是否是nil，如果是，则返回nil
	// 如果不是，则调用fmt.Errorf

	for _, arg := range a {
		if _, ok := arg.(error); ok {
			return fmt.Errorf(format, a...)
		}
	}

	return nil
}
