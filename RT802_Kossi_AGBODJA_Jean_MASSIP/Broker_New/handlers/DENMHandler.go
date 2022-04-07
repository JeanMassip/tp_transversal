package handlers

import (
	"encoding/json"
	"fmt"
)

type DENMHandler struct{}

func NewDENMHandler() *DENMHandler {
	return &DENMHandler{}
}

func (handler *DENMHandler) HandleMessage(message string) error {
	var event EventMesssage
	if err := json.Unmarshal([]byte(message), &event); err != nil {
		return err
	}

	fmt.Println(message)

	return nil
}
