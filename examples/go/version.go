package main

import (
	"runtime/debug"
	"strings"
)

// Version returns the module version from build info, or the stub fallback.
func Version() string {
	info, ok := debug.ReadBuildInfo()
	if ok {
		v := strings.TrimPrefix(info.Main.Version, "v")
		if v != "" && v != "(devel)" {
			return v
		}
	}
	return AppVersion
}

// ModulePath returns the Go module path from build info when present.
func ModulePath() string {
	info, ok := debug.ReadBuildInfo()
	if ok && info.Main.Path != "" {
		return info.Main.Path
	}
	if ok && info.Path != "" {
		return info.Path
	}
	return "github.com/example/agent-bootstrap-hello"
}
