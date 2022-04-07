package handlers

const (
	DENM_NORMAL       uint = 1
	DENM_ROADWORD     uint = 3
	DENM_ACCIDENT     uint = 4
	DENM_TRAFFICJAM   uint = 5
	DENM_SLIPPERYROAD uint = 6
	DENM_FOG          uint = 7
)

type Vehicule struct {
	StationID   string `json:"station_id"`
	StationType uint   `json:"station_type"`
	Speed       uint   `json:"speed"`
	Heading     int    `json:"heading"`
	Position    string `json:"position"`
	LastSeen    string `json:"last_seen,omitempty"`
	Slowed      bool   `json:"slowed,omitempty"`
}

type EventMesssage struct {
	StationID   string `json:"station_id"`
	StationType uint   `json:"station_type"`
	CauseCode   uint   `json:"cause_code"`
	CauseName   string `json:"cause_name"`
	Position    string `json:"position"`
	Time        string `json:"time"`
}
