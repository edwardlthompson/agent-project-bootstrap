package main

import (
	"bytes"
	"encoding/json"
	"strings"
	"testing"
)

func TestReadyJSON(t *testing.T) {
	if ReadyJSON() != `{"status":"ok"}` {
		t.Fatalf("ready: %s", ReadyJSON())
	}
}

func TestRunReadyFlag(t *testing.T) {
	out, err := &bytes.Buffer{}, &bytes.Buffer{}
	if code := Run([]string{"--ready"}, out, err); code != 0 {
		t.Fatalf("exit %d", code)
	}
	if strings.TrimSpace(out.String()) != ReadyJSON() {
		t.Fatalf("stdout %q", out.String())
	}
	var line map[string]string
	if json.Unmarshal([]byte(strings.TrimSpace(err.String())), &line) != nil {
		t.Fatalf("stderr not json: %q", err.String())
	}
	if line["level"] != "info" || line["msg"] != "ready" {
		t.Fatalf("log %v", line)
	}
}

func TestRunDefaultStillGreets(t *testing.T) {
	out, err := &bytes.Buffer{}, &bytes.Buffer{}
	if code := Run(nil, out, err); code != 0 {
		t.Fatalf("exit %d", code)
	}
	if !strings.Contains(out.String(), Greet()) {
		t.Fatalf("stdout %q", out.String())
	}
	if !strings.Contains(err.String(), `"msg":"start"`) {
		t.Fatalf("stderr %q", err.String())
	}
}
