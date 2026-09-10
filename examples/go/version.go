package main

import (
	"runtime/debug"
	"strings"
)

// AppVersion is the stub fallback when build info has no release tag.
const AppVersion = "0.1.0"

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
