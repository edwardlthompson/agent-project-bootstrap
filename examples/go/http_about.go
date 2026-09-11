package main

import (
	"net/http"
)

// AboutHandler serves GET /about with the shared About JSON contract.
func AboutHandler(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodGet {
		http.Error(w, "method not allowed", http.StatusMethodNotAllowed)
		return
	}
	raw, err := AboutPayloadJSON()
	if err != nil {
		http.Error(w, "encode failed", http.StatusInternalServerError)
		return
	}
	w.Header().Set("Content-Type", "application/json; charset=utf-8")
	_, _ = w.Write(raw)
}

// NewAboutMux returns a mux with /about (and optional /health).
func NewAboutMux() *http.ServeMux {
	mux := http.NewServeMux()
	mux.HandleFunc("/about", AboutHandler)
	mux.HandleFunc("/health", func(w http.ResponseWriter, _ *http.Request) {
		w.Header().Set("Content-Type", "application/json; charset=utf-8")
		_, _ = w.Write([]byte(`{"status":"ok"}`))
	})
	return mux
}
