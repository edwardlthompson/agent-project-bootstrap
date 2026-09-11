package main

import (
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"strings"
	"testing"
)

func TestAboutHTTPContract(t *testing.T) {
	req := httptest.NewRequest(http.MethodGet, "/about", nil)
	rr := httptest.NewRecorder()
	NewAboutMux().ServeHTTP(rr, req)
	if rr.Code != http.StatusOK {
		t.Fatalf("status %d", rr.Code)
	}
	ct := rr.Header().Get("Content-Type")
	if !strings.HasPrefix(ct, "application/json") {
		t.Fatalf("content-type: %q", ct)
	}
	var payload AboutPayload
	if err := json.Unmarshal(rr.Body.Bytes(), &payload); err != nil {
		t.Fatal(err)
	}
	if payload.Version == "" || payload.Donate == "" || payload.Update.Status != "current" {
		t.Fatalf("contract fields: %+v", payload)
	}
	if payload.Update.Version != nil || payload.Update.URL != nil {
		t.Fatalf("update stubs must be null: %+v", payload.Update)
	}
}

func TestAboutHTTPMethodNotAllowed(t *testing.T) {
	req := httptest.NewRequest(http.MethodPost, "/about", nil)
	rr := httptest.NewRecorder()
	AboutHandler(rr, req)
	if rr.Code != http.StatusMethodNotAllowed {
		t.Fatalf("status %d", rr.Code)
	}
}
