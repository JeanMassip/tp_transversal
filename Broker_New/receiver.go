package main

import (
	"fmt"
	"math/rand"

	mqtt "github.com/eclipse/paho.mqtt.golang"
)

type Receiver struct {
	MessageChan           chan *string
	Client                mqtt.Client
	MessageHandler        func(client mqtt.Client, msg mqtt.Message)
	ConnectHandler        func(client mqtt.Client)
	ConnectionLostHandler func(client mqtt.Client, err error)
}

func New() (*Receiver, error) {
	r := Receiver{
		MessageChan: make(chan *string),
	}

	r.ConnectionLostHandler = func(client mqtt.Client, err error) {
		fmt.Printf("Connection to Broker lost : %v\n", err)
		close(r.MessageChan)
	}

	r.ConnectHandler = func(client mqtt.Client) {
		fmt.Println("Connected !")
	}

	r.MessageHandler = func(client mqtt.Client, msg mqtt.Message) {
		strMsg := string(msg.Payload())
		fmt.Printf("message received : %s\n", strMsg)
		r.MessageChan <- &strMsg
	}

	return &r, nil
}

func (r Receiver) Connect() {
	var broker = "mosquitto"
	var port = 1883
	opts := mqtt.NewClientOptions()
	opts.AddBroker(fmt.Sprintf("tcp://%s:%d", broker, port))
	opts.SetClientID(fmt.Sprintf("receiver-%d", rand.Intn(1000)))
	opts.SetDefaultPublishHandler(r.MessageHandler)
	opts.OnConnect = r.ConnectHandler
	opts.OnConnectionLost = r.ConnectionLostHandler
	r.Client = mqtt.NewClient(opts)
	if token := r.Client.Connect(); token.Wait() && token.Error() != nil {
		panic(token.Error())
	}
}
