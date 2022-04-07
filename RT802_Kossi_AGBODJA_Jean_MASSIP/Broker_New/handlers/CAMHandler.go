package handlers

import (
	"encoding/json"
	"fmt"
	"math/rand"
	"time"

	mqtt "github.com/eclipse/paho.mqtt.golang"
)

type CAMHandler struct {
	Client    mqtt.Client
	Vehicules map[string]Vehicule
	NbSlowed  uint
	Slowed    bool
}

func NewCAMHandler() *CAMHandler {
	opts := mqtt.NewClientOptions()
	opts.AddBroker("tcp://127.0.0.1:1883")
	opts.SetClientID(fmt.Sprintf("handler-%d", rand.Intn(1000)))
	client := mqtt.NewClient(opts)
	if token := client.Connect(); token.Wait() && token.Error() != nil {
		panic(token.Error())
	}

	return &CAMHandler{
		Client:    client,
		Vehicules: make(map[string]Vehicule),
		NbSlowed:  0,
		Slowed:    false,
	}
}

func (handler *CAMHandler) HandleMessage(message string) error {
	var vehicule Vehicule
	if err := json.Unmarshal([]byte(message), &vehicule); err != nil {
		return err
	}

	fmt.Println("Sensors Message Received - Handling...")

	if vec, ok := handler.Vehicules[vehicule.StationID]; ok {
		vec.LastSeen = time.Now().UTC().String()
		vec.Speed = vehicule.Speed
		vec.Heading = vehicule.Heading
		vec.Position = vehicule.Position
		handler.CheckSpeed()
		fmt.Println("Message Handled")
	}

	return nil
}

func (handler *CAMHandler) CheckSpeed() {
	var nbSlowed uint = 0
	var lastIndex string

	for index, vec := range handler.Vehicules {
		if vec.Speed < 80 {
			nbSlowed++
			lastIndex = index
		}
	}

	if nbSlowed > 2 {
		handler.SendSlowedEvent(lastIndex)
		handler.Slowed = true
	} else if handler.Slowed && nbSlowed < 3 {
		handler.SendNormalEvent(lastIndex)
		handler.Slowed = false
	}
}

func (handler *CAMHandler) SendSlowedEvent(index string) error {
	vec := handler.Vehicules[index]
	message := EventMesssage{
		StationID:   vec.StationID,
		StationType: vec.StationType,
		CauseCode:   DENM_TRAFFICJAM,
		CauseName:   "Ralentissements",
		Position:    vec.Position,
		Time:        time.Now().Format("02/01/06 15:04:05"),
	}

	jsonMessage, err := json.Marshal(message)
	if err != nil {
		return err
	}

	token := handler.Client.Publish("/gw/events", 0, false, jsonMessage)
	token.Wait()

	return nil
}

func (handler *CAMHandler) SendNormalEvent(index string) error {
	vec := handler.Vehicules[index]
	message := EventMesssage{
		StationID:   vec.StationID,
		StationType: vec.StationType,
		CauseCode:   DENM_NORMAL,
		CauseName:   "Normal",
		Position:    vec.Position,
		Time:        time.Now().Format("02/01/06 15:04:05"),
	}

	jsonMessage, err := json.Marshal(message)
	if err != nil {
		return err
	}

	token := handler.Client.Publish("/gw/events", 0, false, jsonMessage)
	token.Wait()

	return nil
}

func (handler *CAMHandler) AddVehicule(vec Vehicule) {
	handler.Vehicules[vec.StationID] = vec
}
