package main

import "encoding/json"

const (
	AppVersion = "0.1.0"
	DonateURL  = "https://github.com/sponsors"
)

// AboutUpdate is the shared update stub on the About JSON payload.
type AboutUpdate struct {
	Status  string  `json:"status"`
	Version *string `json:"version"`
	URL     *string `json:"url"`
}

// AboutPayload is the shared About/donate/update JSON object.
type AboutPayload struct {
	Version string      `json:"version"`
	Donate  string      `json:"donate"`
	Summary string      `json:"summary"`
	Update  AboutUpdate `json:"update"`
}

// AboutSummary is the CLI About slice (version + donate, no crash payload).
func AboutSummary() string {
	return "golden-path " + Version() + " donate " + DonateURL
}

// NewAboutPayload returns the current stub payload (update status current).
func NewAboutPayload() AboutPayload {
	return AboutPayload{
		Version: Version(),
		Donate:  DonateURL,
		Summary: AboutSummary(),
		Update:  AboutUpdate{Status: "current"},
	}
}

// AboutPayloadJSON encodes the shared About contract.
func AboutPayloadJSON() ([]byte, error) {
	return json.Marshal(NewAboutPayload())
}
