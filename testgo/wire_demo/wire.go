//go:build wireinject
// +build wireinject

package main

import (
	"ttt/wire_demo"

	"github.com/google/wire"
)

var Set = wire.NewSet(
	wire.Struct(new(wire_demo.Demost), "*"),
	wire.Struct(new(wire_demo.Demo), "*"),
)

func InitializeFooBar() *wire_demo.Demo {
	wire.Build(Set)
	return nil
}
