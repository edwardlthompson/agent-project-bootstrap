package main

import (
	"encoding/json"
	"fmt"
	"io"
)

// ReadyJSON is the shared CLI readiness payload.
func ReadyJSON() string {
	return `{"status":"ok"}`
}

// LogJSON returns one structured log line (no PII).
func LogJSON(level, msg string) string {
	raw, err := json.Marshal(map[string]string{"level": level, "msg": msg})
	if err != nil {
		return `{"level":"error","msg":"log"}`
	}
	return string(raw)
}

// Run is the CLI entry (stdout = user payload, stderr = JSON logs).
func Run(args []string, stdout, stderr io.Writer) int {
	for _, arg := range args {
		if arg == "--ready" {
			fmt.Fprintln(stderr, LogJSON("info", "ready"))
			fmt.Fprintln(stdout, ReadyJSON())
			return 0
		}
	}
	fmt.Fprintln(stderr, LogJSON("info", "start"))
	fmt.Fprintln(stdout, Greet())
	fmt.Fprintln(stdout, AboutSummary())
	return 0
}
